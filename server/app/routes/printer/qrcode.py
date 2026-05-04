from fastapi import APIRouter, Depends, File, Form, Request, UploadFile

from server.app.bootstrap import get_job_manager, get_device_name
from server.app.schemas.jobs import PrintResponse
from server.app.schemas.preview import PreviewResponse
from server.app.services.jobs.job_manager import JobManager
from server.app.services.printer.qrcode_service import print_qr_code, preview_qr_code

router = APIRouter(prefix="/api", tags=["QR Code"])


@router.post("/qrcode/preview", response_model=PreviewResponse)
async def preview_qrcode(
    url: str = Form(...),
    size: int = Form(384),
    style: str = Form("square"),
    embed_image: UploadFile | None = File(None),
):
    image_data = await embed_image.read() if embed_image else None
    return preview_qr_code(url, size, style, image_data)


@router.post("/qrcode", response_model=PrintResponse, status_code=201)
async def print_qrcode(
    url: str = Form(...),
    size: int = Form(384),
    style: str = Form("square"),
    embed_image: UploadFile | None = File(None),
    job_manager: JobManager = Depends(get_job_manager),
    device_name: str = Depends(get_device_name),
):
    image_data = await embed_image.read() if embed_image else None
    job = print_qr_code(url, size, job_manager, device_name, style, image_data)
    return PrintResponse(job_id=job.job_id, status=job.status)
