from fastapi import APIRouter, Depends

from server.app.dependencies import get_job_manager
from server.app.schemas.jobs import PrintResponse, QRCodeRequest
from server.app.services.job_manager import JobManager
from server.app.services.qrcode_service import print_qr_code

router = APIRouter(prefix="/api", tags=["QR Code"])


@router.post("/qrcode", response_model=PrintResponse, status_code=201)
async def print_qrcode(
    body: QRCodeRequest,
    job_manager: JobManager = Depends(get_job_manager),
):
    job = print_qr_code(str(body.url), body.size, job_manager)
    return PrintResponse(job_id=job.job_id, status=job.status)
