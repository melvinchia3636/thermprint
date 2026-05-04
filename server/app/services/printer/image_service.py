"""Image print-job creation (photo / picture mode).

Processes an uploaded image file into printer nibble data and a preview PNG,
then creates a print job via :class:`JobManager`.
"""

import tempfile

from fastapi import UploadFile, HTTPException

from thermal_printer.image_processor import process_image
from thermal_printer.simulator import simulate_print
from server.app.schemas.print_settings import PrintSettings
from server.app.services.jobs.job_manager import JobManager, JobType
from io import BytesIO


def print_image(
    image: UploadFile,
    settings: PrintSettings,
    device_name: str,
    job_manager: JobManager,
):
    """Process an uploaded image and enqueue it as a new print job.

    Validates the file type, applies the image-processing pipeline
    (resize, contrast, gamma, dither, nibble-encode), generates a preview PNG,
    and delegates to ``job_manager.create_job``.
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
