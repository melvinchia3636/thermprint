import tempfile
from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException

from thermal_printer.image_processor import process_image
from thermal_printer.simulator import simulate_print
from server.app.schemas.print_settings import PrintSettings
from server.app.schemas.preview import PreviewResponse

router = APIRouter(prefix="/api", tags=["Preview"])


def _parse_print_settings(
    ble_device_name: str = Form("X5h-10B5"),
    width: int = Form(384),
    quality: int = Form(0x32),
    speed: int = Form(0x10),
    energy: int = Form(0),
    contrast: float = Form(1.0),
    gamma: float = Form(1.0),
    rotate: int = Form(0),
    chunk_rows: int = Form(10),
    chunk_delay: float = Form(0.2),
    feed: int = Form(200),
) -> PrintSettings:
    return PrintSettings(
        ble_device_name=ble_device_name,
        width=width,
        quality=quality,
        speed=speed,
        energy=energy,
        contrast=contrast,
        gamma=gamma,
        rotate=rotate,
        chunk_rows=chunk_rows,
        chunk_delay=chunk_delay,
        feed=feed,
    )


def _process_image_helper(
    image: UploadFile,
    settings: PrintSettings,
) -> tuple:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=422, detail="File must be an image")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image.file.read())
        tmp_path = tmp.name

    try:
        nibble_data, width, height, dithered = process_image(
            image_path=tmp_path,
            printer_width=settings.width,
            contrast=settings.contrast,
            gamma=settings.gamma,
            rotate=settings.rotate,
        )
    finally:
        import os

        os.unlink(tmp_path)

    return nibble_data, width, height, dithered


@router.post("/preview", response_model=PreviewResponse)
async def preview_image(
    image: UploadFile = File(..., description="Image file to process for preview"),
    settings: PrintSettings = Depends(_parse_print_settings),
):
    nibble_data, width, height, dithered = _process_image_helper(image, settings)

    buf = BytesIO()
    simulate_print(dithered, width, height, buf)
    return PreviewResponse.from_preview_image(buf, width, height)
