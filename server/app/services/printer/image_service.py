"""Image print-job creation (photo / picture mode).

Processes an uploaded image file into printer nibble data and a preview PNG,
then creates a print job via :class:`JobManager`.
"""

import tempfile
from io import BytesIO

from PIL import Image, ImageDraw
from fastapi import UploadFile, HTTPException

from lib.thermal_printer.image_processor import process_image, gray_to_nibbles
from lib.thermal_printer.simulator import simulate_print
from server.app.schemas.print_settings import PrintSettings
from server.app.services.jobs.job_manager import JobManager, JobType

DASH_GAP = 8
DASH_LENGTH = 8


def _build_print_strip(
    img: Image.Image, cols: int, rows: int, printer_width: int
) -> tuple[bytes, bytes, int, int]:
    """Stack cells vertically in reading order with dashed separators.

    Returns ``(nibble_data, preview_bytes, strip_width, strip_height)``.
    """
    w, h = img.size
    cell_w = w // cols
    cell_h = h // rows

    total = cols * rows
    canvas_h = total * cell_h

    canvas = Image.new("L", (printer_width, canvas_h), 255)
    draw = ImageDraw.Draw(canvas)

    for idx in range(total):
        r = idx // cols
        c = idx % cols

        left = c * cell_w
        top = r * cell_h
        cell = img.crop((left, top, left + cell_w, top + cell_h))

        y_offset = idx * cell_h
        canvas.paste(cell, (0, y_offset))

    for idx in range(total - 1):
        sep_y = (idx + 1) * cell_h
        draw.line([(0, sep_y), (printer_width, sep_y)], fill=0, width=2)
        for x in range(0, printer_width, DASH_GAP * 2):
            draw.line(
                [(x, sep_y), (x + DASH_LENGTH, sep_y)],
                fill=255,
                width=2,
            )

    pixels = list(canvas.getdata())
    nibble_data = gray_to_nibbles(pixels, printer_width, canvas_h)

    buf = BytesIO()
    canvas.save(buf, format="PNG")

    return nibble_data, printer_width


def _draw_annotated_preview(img: Image.Image, cols: int, rows: int) -> bytes:
    """Return PNG bytes of the preview image with red dashed split lines."""
    annotated = img.convert("RGB")
    draw = ImageDraw.Draw(annotated)
    w, h = annotated.size
    cell_w = w // cols
    cell_h = h // rows

    for i in range(1, cols):
        x = i * cell_w
        for y in range(0, h, 12):
            draw.line([(x, y), (x, y + 6)], fill=(255, 0, 0), width=1)

    for j in range(1, rows):
        y = j * cell_h
        for x in range(0, w, 12):
            draw.line([(x, y), (x + 6, y)], fill=(255, 0, 0), width=1)

    buf = BytesIO()
    annotated.save(buf, format="PNG")
    return buf.getvalue()


def print_image(
    image: UploadFile,
    settings: PrintSettings,
    device_name: str,
    job_manager: JobManager,
):
    """Process an uploaded image and enqueue it as a new print job.

    When *split_cols* / *split_rows* > 1 the image is processed at
    ``width × split_cols`` and the cells are stacked vertically as a long
    receipt strip with dashed separators.
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

    # ---- generate preview PNG ----
    if settings.split_cols > 1 or settings.split_rows > 1:
        buf = BytesIO()
        simulate_print(dithered, width, height, buf)
        full_preview = Image.open(buf)

        aug_preview = _draw_annotated_preview(
            full_preview, settings.split_cols, settings.split_rows
        )

        nibble_data, strip_w = _build_print_strip(
            full_preview, settings.split_cols, settings.split_rows, settings.width
        )
        width = strip_w
        preview_image = aug_preview
    else:
        buf = BytesIO()
        simulate_print(dithered, width, height, buf)
        preview_image = buf.getvalue()

    return job_manager.create_job(
        JobType.image,
        nibble_data=nibble_data,
        width=width,
        settings={
            "ble_device_name": device_name,
            "quality": settings.quality,
            "speed": settings.speed,
            "energy": settings.energy,
            "chunk_rows": settings.chunk_rows,
            "chunk_delay": settings.chunk_delay,
            "feed": settings.feed,
        },
        preview_image=preview_image,
    )
