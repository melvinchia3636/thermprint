from fastapi import APIRouter, Depends, HTTPException, Query

from server.app.bootstrap import get_job_manager
from server.app.schemas.jobs import JobStatusResponse, JobListResponse
from server.app.services.jobs.job_manager import JobManager

router = APIRouter(prefix="/api", tags=["Jobs"])


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    job_manager: JobManager = Depends(get_job_manager),
):
    jobs, total = await job_manager.list_jobs(offset, limit)
    return JobListResponse(jobs=jobs, total=total)


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
        type=job.job_type,
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
        raise HTTPException(
            status_code=404, detail="Job not found or already in progress"
        )


@router.delete("/jobs/{job_id}/delete", status_code=204)
async def delete_job(
    job_id: str,
    job_manager: JobManager = Depends(get_job_manager),
):
    if not await job_manager.delete_job(job_id):
        raise HTTPException(
            status_code=404, detail="Job not found or cannot be deleted"
        )
