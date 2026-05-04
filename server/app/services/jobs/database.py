"""SQLite persistence for print job history.

Stores job metadata (status, progress, error, preview image, settings) in a local
SQLite database so the queue survives server restarts.  Exposes paginated listing
used by the ``GET /api/jobs`` endpoint.
"""

import base64
import json
import logging
from pathlib import Path

import aiosqlite

from server.app.schemas.jobs import JobStatus, JobType, JobStatusResponse

logger = logging.getLogger(__name__)

_DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "jobs.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    status TEXT NOT NULL,
    progress TEXT,
    error TEXT,
    created_at TEXT NOT NULL,
    preview_image BLOB,
    settings TEXT
)
"""


class DatabaseService:
    """Async SQLite wrapper for the print job history table."""

    def __init__(self, db_path: str | None = None):
        self._path = Path(db_path) if db_path else _DB_PATH
        self._conn: aiosqlite.Connection | None = None

    async def start(self):
        """Open the database connection and ensure the schema exists."""
        self._conn = await aiosqlite.connect(str(self._path))
        await self._conn.execute(CREATE_TABLE_SQL)
        await self._conn.commit()
        logger.info("Database initialized at %s", self._path)

    async def stop(self):
        """Close the database connection."""
        if self._conn:
            await self._conn.close()

    async def insert_job(
        self,
        job_id: str,
        job_type: JobType,
        status: JobStatus,
        created_at: str,
        preview_image: bytes | None = None,
        settings: dict | None = None,
    ):
        """Insert a new job row."""
        await self._conn.execute(
            "INSERT INTO jobs (job_id, type, status, progress, error, created_at, preview_image, settings) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                job_id,
                job_type.value,
                status.value,
                None,
                None,
                created_at,
                preview_image,
                json.dumps(settings) if settings else None,
            ),
        )
        await self._conn.commit()

    async def update_job(
        self,
        job_id: str,
        status: JobStatus | None = None,
        progress: str | None = None,
        error: str | None = None,
        preview_image: bytes | None = None,
    ):
        """Update one or more fields of an existing job row.

        Only the fields that are not ``None`` will be written.
        """
        parts = []
        params = []
        if status is not None:
            parts.append("status = ?")
            params.append(status.value)
        if progress is not None:
            parts.append("progress = ?")
            params.append(progress)
        if error is not None:
            parts.append("error = ?")
            params.append(error)
        if preview_image is not None:
            parts.append("preview_image = ?")
            params.append(preview_image)
        if not parts:
            return
        params.append(job_id)
        await self._conn.execute(
            f"UPDATE jobs SET {', '.join(parts)} WHERE job_id = ?",
            params,
        )
        await self._conn.commit()

    async def list_jobs(
        self, offset: int = 0, limit: int = 50
    ) -> tuple[list[JobStatusResponse], int]:
        """Return a paginated slice of jobs (newest first) together with the total count."""
        cursor = await self._conn.execute(
            "SELECT job_id, type, status, progress, error, created_at, preview_image FROM jobs "
            "ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
        rows = await cursor.fetchall()
        jobs = [
            JobStatusResponse(
                job_id=row[0],
                type=JobType(row[1]),
                status=JobStatus(row[2]),
                progress=row[3],
                error=row[4],
                created_at=row[5],
                preview_url=blob_to_data_url(row[6]),
            )
            for row in rows
        ]
        cursor2 = await self._conn.execute("SELECT COUNT(*) FROM jobs")
        total_row = await cursor2.fetchone()
        total = total_row[0] if total_row else 0
        return jobs, total

    async def get_job_status(self, job_id: str) -> JobStatusResponse | None:
        """Fetch a single job by its ID, or ``None`` if it does not exist."""
        cursor = await self._conn.execute(
            "SELECT job_id, type, status, progress, error, created_at, preview_image FROM jobs WHERE job_id = ?",
            (job_id,),
        )
        row = await cursor.fetchone()
        if not row:
            return None
        return JobStatusResponse(
            job_id=row[0],
            type=JobType(row[1]),
            status=JobStatus(row[2]),
            progress=row[3],
            error=row[4],
            created_at=row[5],
            preview_url=blob_to_data_url(row[6]),
        )

    async def delete_job(self, job_id: str) -> bool:
        """Delete a job row. Returns ``True`` if a row was deleted."""
        cursor = await self._conn.execute("DELETE FROM jobs WHERE job_id = ?", (job_id,))
        await self._conn.commit()
        return cursor.rowcount > 0


def blob_to_data_url(blob: bytes | None) -> str | None:
    if not blob:
        return None
    encoded = base64.b64encode(blob).decode()
    return f"data:image/png;base64,{encoded}"
