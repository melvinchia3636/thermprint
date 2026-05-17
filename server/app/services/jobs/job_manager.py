"""Print job lifecycle management.

Defines the :class:`PrintJob` dataclass and the :class:`JobManager` that owns the
print queue, drives the async worker loop, and persists state changes to the
:class:`DatabaseService`.
"""

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from server.app.schemas.jobs import JobStatus, JobType, JobStatusResponse
from server.app.services.jobs.broadcast import BroadcastService
from server.app.services.jobs.database import DatabaseService, blob_to_data_url

logger = logging.getLogger(__name__)


@dataclass
class PrintJob:
    """In-memory representation of a queued / active print job.

    ``nibble_data``, ``cancel_event``, and the Python object identity are
    transient - they only exist while the job is in the active queue.
    Everything else is mirrored to the database.
    """

    job_id: str
    job_type: JobType
    status: JobStatus = JobStatus.queued
    progress: str | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    nibble_data: bytes = b""
    width: int = 0
    settings: dict = field(default_factory=dict)
    cancel_event: asyncio.Event = field(default_factory=asyncio.Event)
    preview_image: bytes | None = None


class JobManager:
    """Owns the print job queue, runs the worker loop, and broadcasts status changes."""

    def __init__(self, printer_manager, db: DatabaseService, loop=None):
        self._printer_manager = printer_manager
        self._db = db
        self._loop = loop or asyncio.get_event_loop()
        self._jobs: dict[str, PrintJob] = {}
        self._queue: asyncio.Queue[str] = asyncio.Queue()
        self._worker_task: asyncio.Task | None = None
        self._broadcast = BroadcastService()

    def subscribe(self) -> asyncio.Queue[str]:
        """Return a new subscriber queue that receives JSON job-status payloads."""
        return self._broadcast.subscribe()

    def unsubscribe(self, q: asyncio.Queue[str]):
        """Remove a subscriber queue."""
        self._broadcast.unsubscribe(q)

    def _notify(self, job: PrintJob):
        """Serialize the job's current state as JSON and publish it to all subscribers."""
        preview_url = blob_to_data_url(job.preview_image)
        self._broadcast.publish(
            JobStatusResponse(
                job_id=job.job_id,
                type=job.job_type,
                status=job.status,
                progress=job.progress,
                error=job.error,
                created_at=job.created_at,
                preview_url=preview_url,
            ).model_dump_json()
        )

    def start(self):
        """Launch the background worker coroutine."""
        self._worker_task = self._loop.create_task(self._worker())

    async def stop(self):
        """Cancel the worker and close the database connection."""
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        await self._db.stop()

    def create_job(
        self,
        job_type: JobType,
        nibble_data: bytes,
        width: int,
        settings: dict,
        preview_image: bytes | None = None,
    ) -> PrintJob:
        """Create a new print job, enqueue it, persist to DB, and notify subscribers."""
        job = PrintJob(
            job_id=str(uuid.uuid4()),
            job_type=job_type,
            nibble_data=nibble_data,
            width=width,
            settings=settings,
            preview_image=preview_image,
        )
        self._jobs[job.job_id] = job
        self._queue.put_nowait(job.job_id)
        self._notify(job)
        asyncio.ensure_future(
            self._db.insert_job(
                job_id=job.job_id,
                job_type=job_type,
                status=job.status,
                created_at=job.created_at.isoformat(),
                preview_image=preview_image,
                settings=settings,
            )
        )
        return job

    def get_job(self, job_id: str) -> PrintJob | None:
        """Return the in-memory job, or ``None`` if it does not exist."""
        return self._jobs.get(job_id)

    async def list_jobs(
        self, offset: int = 0, limit: int = 50
    ) -> tuple[list[JobStatusResponse], int]:
        """Return a paginated list and total count."""
        return await self._db.list_jobs(offset, limit)

    def cancel_job(self, job_id: str) -> bool:
        """Cancel an active job. Returns ``False`` if the job can't be cancelled."""
        job = self._jobs.get(job_id)
        if not job:
            return False
        if job.status in (JobStatus.done, JobStatus.failed, JobStatus.cancelled):
            return False
        job.status = JobStatus.cancelled
        job.progress = None
        job.cancel_event.set()
        self._notify(job)
        asyncio.ensure_future(
            self._db.update_job(job_id, status=JobStatus.cancelled, progress=None)
        )
        return True

    async def delete_job(self, job_id: str) -> bool:
        """Delete a job from the database. Only allowed for terminal jobs."""
        job = self._jobs.get(job_id)
        if job and job.status not in (
            JobStatus.done,
            JobStatus.failed,
            JobStatus.cancelled,
        ):
            return False
        self._jobs.pop(job_id, None)
        return await self._db.delete_job(job_id)

    async def _worker(self):
        """Background loop: pull jobs from the queue, connect, and print."""
        while True:
            job_id = await self._queue.get()
            job = self._jobs.get(job_id)
            if not job or job.status != JobStatus.queued:
                continue

            try:
                job.status = JobStatus.connecting
                self._notify(job)
                await self._db.update_job(job_id, status=JobStatus.connecting)

                if job.cancel_event.is_set():
                    continue

                total_chunks = 0

                def progress_callback(current, total):
                    nonlocal total_chunks
                    total_chunks = total
                    if job.cancel_event.is_set():
                        return
                    job.progress = f"{current}/{total} chunks"
                    self._notify(job)

                def connection_callback():
                    if not job.cancel_event.is_set():
                        job.status = JobStatus.printing
                        self._notify(job)
                        asyncio.ensure_future(
                            self._db.update_job(job_id, status=JobStatus.printing)
                        )

                await self._printer_manager.print_job(
                    nibble_data=job.nibble_data,
                    width=job.width,
                    progress_callback=progress_callback,
                    cancel_event=job.cancel_event,
                    connection_callback=connection_callback,
                    **job.settings,
                )
                if not job.cancel_event.is_set():
                    job.status = JobStatus.done
                    job.progress = None
                    self._notify(job)
                    await self._db.update_job(
                        job_id, status=JobStatus.done, progress=None
                    )
                    logger.info("Job %s completed", job_id)
                    await asyncio.sleep(10)
            except Exception as exc:
                job.status = JobStatus.failed
                job.error = str(exc)
                self._notify(job)
                await self._db.update_job(
                    job_id, status=JobStatus.failed, error=str(exc)
                )
                logger.error("Job %s failed: %s", job_id, exc)
