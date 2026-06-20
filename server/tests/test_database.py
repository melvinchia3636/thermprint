import uuid
from datetime import datetime, timezone

from server.app.schemas.jobs import JobStatus, JobType


class TestDatabaseFailIncomplete:
    async def test_fail_incomplete_marks_queued_as_failed(self, app):
        db = app.state.job_manager._db
        job_id = str(uuid.uuid4())
        await db.insert_job(
            job_id, JobType.image, JobStatus.queued,
            datetime.now(timezone.utc).isoformat(),
        )

        count = await db.fail_incomplete_jobs("Server restarted")
        assert count == 1

        job = await db.get_job_status(job_id)
        assert job.status == JobStatus.failed
        assert job.error == "Server restarted"

    async def test_fail_incomplete_skips_done_jobs(self, app):
        db = app.state.job_manager._db
        job_id = str(uuid.uuid4())
        await db.insert_job(
            job_id, JobType.image, JobStatus.done,
            datetime.now(timezone.utc).isoformat(),
        )

        count = await db.fail_incomplete_jobs("Server restarted")
        assert count == 0

        job = await db.get_job_status(job_id)
        assert job.status == JobStatus.done

    async def test_fail_incomplete_skips_failed_jobs(self, app):
        db = app.state.job_manager._db
        job_id = str(uuid.uuid4())
        await db.insert_job(
            job_id, JobType.image, JobStatus.failed,
            datetime.now(timezone.utc).isoformat(),
        )

        count = await db.fail_incomplete_jobs("Server restarted")
        assert count == 0

    async def test_fail_incomplete_skips_cancelled_jobs(self, app):
        db = app.state.job_manager._db
        job_id = str(uuid.uuid4())
        await db.insert_job(
            job_id, JobType.image, JobStatus.cancelled,
            datetime.now(timezone.utc).isoformat(),
        )

        count = await db.fail_incomplete_jobs("Server restarted")
        assert count == 0

    async def test_fail_incomplete_handles_mixed_statuses(self, app):
        db = app.state.job_manager._db
        now = datetime.now(timezone.utc).isoformat()
        await db.insert_job(str(uuid.uuid4()), JobType.image, JobStatus.queued, now)
        await db.insert_job(str(uuid.uuid4()), JobType.qr_code, JobStatus.printing, now)
        await db.insert_job(str(uuid.uuid4()), JobType.calendar, JobStatus.connecting, now)
        await db.insert_job(str(uuid.uuid4()), JobType.image, JobStatus.done, now)
        await db.insert_job(str(uuid.uuid4()), JobType.qr_code, JobStatus.cancelled, now)

        count = await db.fail_incomplete_jobs("Server restarted")
        assert count == 3
