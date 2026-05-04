import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from server.app.schemas.jobs import JobStatus, JobType, JobStatusResponse
from server.app.services.broadcast import BroadcastService

logger = logging.getLogger(__name__)


@dataclass
class PrintJob:
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


class JobManager:
    def __init__(self, printer_manager, loop=None):
        self._printer_manager = printer_manager
        self._loop = loop or asyncio.get_event_loop()
        self._jobs: dict[str, PrintJob] = {}
        self._queue: asyncio.Queue[str] = asyncio.Queue()
        self._worker_task: asyncio.Task | None = None
        self._broadcast = BroadcastService()

    def subscribe(self) -> asyncio.Queue[str]:
        return self._broadcast.subscribe()

    def unsubscribe(self, q: asyncio.Queue[str]):
        self._broadcast.unsubscribe(q)

    def _notify(self, job: PrintJob):
        self._broadcast.publish(
            JobStatusResponse(
                job_id=job.job_id,
                type=job.job_type,
                status=job.status,
                progress=job.progress,
                error=job.error,
                created_at=job.created_at,
            ).model_dump_json()
        )

    def start(self):
        self._worker_task = self._loop.create_task(self._worker())

    async def stop(self):
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

    def create_job(self, job_type: JobType, nibble_data: bytes, width: int, settings: dict) -> PrintJob:
        job = PrintJob(
            job_id=str(uuid.uuid4()),
            job_type=job_type,
            nibble_data=nibble_data,
            width=width,
            settings=settings,
        )
        self._jobs[job.job_id] = job
        self._queue.put_nowait(job.job_id)
        self._notify(job)
        return job

    def get_job(self, job_id: str) -> PrintJob | None:
        return self._jobs.get(job_id)

    def list_jobs(self) -> list[JobStatusResponse]:
        jobs = sorted(self._jobs.values(), key=lambda j: j.created_at, reverse=True)
        return [
            JobStatusResponse(
                job_id=j.job_id,
                type=j.job_type,
                status=j.status,
                progress=j.progress,
                error=j.error,
                created_at=j.created_at,
            )
            for j in jobs
        ]

    def cancel_job(self, job_id: str) -> bool:
        job = self._jobs.get(job_id)
        if not job:
            return False
        if job.status in (JobStatus.done, JobStatus.failed, JobStatus.cancelled):
            return False
        job.status = JobStatus.cancelled
        job.cancel_event.set()
        self._notify(job)
        return True

    async def _worker(self):
        while True:
            job_id = await self._queue.get()
            job = self._jobs.get(job_id)
            if not job or job.status != JobStatus.queued:
                continue

            try:
                job.status = JobStatus.connecting
                self._notify(job)

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
                    job.progress = f"{total_chunks} chunks printed"
                    self._notify(job)
                    logger.info("Job %s completed", job_id)
            except Exception as exc:
                job.status = JobStatus.failed
                job.error = str(exc)
                self._notify(job)
                logger.error("Job %s failed: %s", job_id, exc)
