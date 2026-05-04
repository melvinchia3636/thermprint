from fastapi import APIRouter, Depends, UploadFile, File

from server.app.dependencies import get_job_manager
from server.app.schemas.print_settings import PrintSettings
from server.app.schemas.jobs import PrintResponse, JobType
from server.app.services.job_manager import JobManager
from server.app.services.preview_service import _process_image_data
from server.app.routes._forms import parse_print_settings

router = APIRouter(prefix="/api", tags=["Print"])


@router.post("/print", response_model=PrintResponse, status_code=201)
async def print_image(
    image: UploadFile = File(..., description="Image file to print"),
    settings: PrintSettings = Depends(parse_print_settings),
    job_manager: JobManager = Depends(get_job_manager),
):
    nibble_data, width, _, _ = _process_image_data(image, settings)

    job = job_manager.create_job(
        JobType.image,
        nibble_data=nibble_data,
        width=width,
        settings={
            "ble_device_name": settings.ble_device_name,
            "quality": settings.quality,
            "speed": settings.speed,
            "energy": settings.energy,
            "chunk_rows": settings.chunk_rows,
            "chunk_delay": settings.chunk_delay,
            "feed": settings.feed,
        },
    )
    return PrintResponse(job_id=job.job_id, status=job.status)
