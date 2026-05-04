"""Preview-image generation for the image-printing workflow.

Provides the shared image-processing pipeline (``_process_image_data``) and
the high-level ``process_preview_image`` function used by the
``POST /api/preview`` endpoint.
"""

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
    """Run the full image-processing pipeline and return raw pixel data.

    Returns ``(nibble_data, width, height, dithered_pixels)``.
    Shared between the preview and print workflows.
    """
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
    """Process an uploaded image and return a base64-encoded preview PNG."""
    _, width, height, dithered = _process_image_data(image, settings)
    buf = BytesIO()
    simulate_print(dithered, width, height, buf)
    return PreviewResponse.from_preview_image(buf, width, height)
