from fastapi import APIRouter, Depends, HTTPException, Request

from server.app.dependencies import get_job_manager
from server.app.schemas.print_settings import PrintSettings
from server.app.schemas.jobs import JobStatusResponse, JobListResponse
from server.app.services.job_manager import JobManager
from server.app.services.settings_store import SettingsStore

router = APIRouter(prefix="/api", tags=["Jobs"])


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    job_manager: JobManager = Depends(get_job_manager),
):
    return JobListResponse(jobs=job_manager.list_jobs())


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job(
    job_id: str,
    job_manager: JobManager = Depends(get_job_manager),
):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(
        job_id=job.job_id,
        status=job.status,
        progress=job.progress,
        error=job.error,
        created_at=job.created_at,
    )


@router.delete("/jobs/{job_id}", status_code=204)
async def cancel_job(
    job_id: str,
    job_manager: JobManager = Depends(get_job_manager),
):
    if not job_manager.cancel_job(job_id):
        raise HTTPException(status_code=404, detail="Job not found or already in progress")


def _get_settings_store(request: Request) -> SettingsStore:
    return request.app.state.settings_store


@router.get("/settings", response_model=PrintSettings)
async def get_settings(
    store: SettingsStore = Depends(_get_settings_store),
):
    return store.load()


@router.put("/settings", response_model=PrintSettings)
async def update_settings(
    settings: PrintSettings,
    store: SettingsStore = Depends(_get_settings_store),
):
    return store.save(settings)
