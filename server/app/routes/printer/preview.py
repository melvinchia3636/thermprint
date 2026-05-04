from fastapi import APIRouter, Depends, UploadFile, File

from server.app.schemas.print_settings import PrintSettings
from server.app.schemas.preview import PreviewResponse
from server.app.services.printer.preview_service import process_preview_image
from server.app.routes.forms import parse_print_settings

router = APIRouter(prefix="/api", tags=["Preview"])


@router.post("/preview", response_model=PreviewResponse)
async def preview_image(
    image: UploadFile = File(..., description="Image file to process for preview"),
    settings: PrintSettings = Depends(parse_print_settings),
):
    return process_preview_image(image, settings)
