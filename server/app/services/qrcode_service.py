import json
import logging
from pathlib import Path

import qrcode
from PIL import Image

from thermal_printer.image_processor import gray_to_nibbles
from server.app.schemas.print_settings import PrintSettings
from server.app.services.job_manager import JobManager, JobType

logger = logging.getLogger(__name__)

_QR_SETTINGS_PATH = Path(__file__).resolve().parent.parent / "configs" / "qrcode.json"


def _load_qr_settings() -> PrintSettings:
    with open(_QR_SETTINGS_PATH) as f:
        return PrintSettings(**json.load(f))


def _auto_box_size(modules_count: int, target: int) -> int:
    return max(1, target // (modules_count + 4))


def print_qr_code(url: str, size: int, job_manager: JobManager):
    settings = _load_qr_settings()
    printer_width = settings.width
    size = max(50, min(printer_width, size))

    qr = qrcode.QRCode(border=2)
    qr.add_data(url)
    qr.make(fit=True)

    box_size = _auto_box_size(qr.modules_count, size)
    qr.border = 2
    qr.box_size = box_size
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("L")
    img = img.resize((size, size), Image.LANCZOS)

    canvas = Image.new("L", (printer_width, size), 255)
    offset = (printer_width - size) // 2
    canvas.paste(img, (offset, 0))
    pixels = list(canvas.getdata())

    nibble_data = gray_to_nibbles(pixels, printer_width, size)

    return job_manager.create_job(
        JobType.qr_code,
        nibble_data=nibble_data,
        width=printer_width,
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
