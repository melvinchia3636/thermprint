import tempfile

from fastapi import UploadFile, HTTPException

from thermal_printer.image_processor import process_image
from thermal_printer.simulator import simulate_print
from server.app.schemas.print_settings import PrintSettings
from server.app.schemas.preview import PreviewResponse
from io import BytesIO


def _process_image_data(
    image: UploadFile,
    settings: PrintSettings,
) -> tuple[bytes, int, int]:
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


def process_preview_image(
    image: UploadFile,
    settings: PrintSettings,
) -> PreviewResponse:
    nibble_data, width, height, dithered = _process_image_data(image, settings)
    buf = BytesIO()
    simulate_print(dithered, width, height, buf)
    return PreviewResponse.from_preview_image(buf, width, height)
