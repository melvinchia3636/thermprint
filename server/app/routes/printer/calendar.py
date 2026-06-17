from fastapi import APIRouter, Depends, Form

from server.app.bootstrap import get_job_manager, get_device_name
from server.app.schemas.jobs import PrintResponse
from server.app.schemas.preview import PreviewResponse
from server.app.services.jobs.job_manager import JobManager
from server.app.services.printer.calendar_service import preview_calendar, print_calendar

router = APIRouter(prefix="/api", tags=["Calendar"])


@router.post("/calendar/preview", response_model=PreviewResponse)
async def preview_calendar_route(
    year: int = Form(..., ge=2000, le=2100),
    month: int = Form(..., ge=1, le=12),
):
    return preview_calendar(year, month)


@router.post("/calendar", response_model=PrintResponse, status_code=201)
async def print_calendar_route(
    year: int = Form(..., ge=2000, le=2100),
    month: int = Form(..., ge=1, le=12),
    job_manager: JobManager = Depends(get_job_manager),
    device_name: str = Depends(get_device_name),
):
    job = print_calendar(year, month, job_manager, device_name)
    return PrintResponse(job_id=job.job_id, status=job.status)
