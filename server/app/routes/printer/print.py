from fastapi import APIRouter, Depends, UploadFile, File

from server.app.bootstrap import get_job_manager, get_device_name
from server.app.schemas.print_settings import PrintSettings
from server.app.schemas.jobs import PrintResponse
from server.app.services.jobs.job_manager import JobManager
from server.app.services.printer.image_service import print_image
from server.app.routes.forms import parse_print_settings

router = APIRouter(prefix="/api", tags=["Print"])


@router.post("/print", response_model=PrintResponse, status_code=201)
async def print_image_endpoint(
    image: UploadFile = File(..., description="Image file to print"),
    settings: PrintSettings = Depends(parse_print_settings),
    job_manager: JobManager = Depends(get_job_manager),
    device_name: str = Depends(get_device_name),
):
    job = print_image(image, settings, device_name, job_manager)
    return PrintResponse(job_id=job.job_id, status=job.status)
