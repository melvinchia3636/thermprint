"""Preview-image generation for the image-printing workflow.

Provides the shared image-processing pipeline (``_process_image_data``) and
the high-level ``process_preview_image`` function used by the
``POST /api/preview`` endpoint.
"""

import tempfile
from io import BytesIO

from PIL import Image, ImageDraw
from fastapi import UploadFile, HTTPException

from lib.thermal_printer.image_processor import process_image
from lib.thermal_printer.simulator import simulate_print
from server.app.schemas.print_settings import PrintSettings
from server.app.schemas.preview import PreviewResponse

PRINTER_WIDTH = 384


def _draw_split_lines(img: Image.Image, cols: int, rows: int) -> Image.Image:
    """Return a copy of *img* with red dashed split-grid lines overlaid."""
    annotated = img.convert("RGB")
    draw = ImageDraw.Draw(annotated)
    w, h = annotated.size
    cell_w = w // cols
    cell_h = h // rows

    for i in range(1, cols):
        x = i * cell_w
        for y in range(0, h, 12):
            draw.line([(x, y), (x, y + 6)], fill=(255, 0, 0), width=2)

    for j in range(1, rows):
        y = j * cell_h
        for x in range(0, w, 12):
            draw.line([(x, y), (x + 6, y)], fill=(255, 0, 0), width=2)

    return annotated


def _process_image_data(
    image: UploadFile,
    settings: PrintSettings,
) -> tuple[bytes, int, int, list[int]]:
    """Run the full image-processing pipeline and return raw pixel data.

    Returns ``(nibble_data, width, height, dithered_pixels)``.
    When *split_cols* > 1 the target width is multiplied accordingly.
    """
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=422, detail="File must be an image")

    target_width = settings.width * settings.split_cols

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image.file.read())
        tmp_path = tmp.name

    try:
        nibble_data, width, height, dithered = process_image(
            image_path=tmp_path,
            printer_width=target_width,
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
    """Process an uploaded image and return a base64-encoded preview PNG.

    When splits are active the preview includes red dashed grid lines.
    """
    _, width, height, dithered = _process_image_data(image, settings)

    buf = BytesIO()
    simulate_print(dithered, width, height, buf)

    if settings.split_cols > 1 or settings.split_rows > 1:
        preview = Image.open(buf)
        annotated = _draw_split_lines(preview, settings.split_cols, settings.split_rows)
        buf = BytesIO()
        annotated.save(buf, format="PNG")

    return PreviewResponse.from_preview_image(buf, width, height)
