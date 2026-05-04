"""QR-code print-job creation.

Generates a QR code from a URL, renders it with optional styling and an
optional embedded logo image, converts the result to printer nibble data, and
creates a print job.  Also provides a standalone preview function used by the
``POST /api/qrcode/preview`` endpoint.
"""

import json
import logging
from io import BytesIO
from pathlib import Path

import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    CircleModuleDrawer,
    GappedSquareModuleDrawer,
    HorizontalBarsDrawer,
    RoundedModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
)
from qrcode.image.styles.colormasks import SolidFillColorMask

from thermal_printer.image_processor import gray_to_nibbles
from server.app.schemas.print_settings import PrintSettings
from server.app.schemas.preview import PreviewResponse
from server.app.services.jobs.job_manager import JobManager, JobType

logger = logging.getLogger(__name__)

_QR_SETTINGS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "qrcode.json"


def _load_qr_settings() -> PrintSettings:
    with open(_QR_SETTINGS_PATH) as f:
        return PrintSettings(**json.load(f))


def _auto_box_size(modules_count: int, target: int) -> int:
    return max(1, target // (modules_count + 4))


_DRAWERS = {
    "square": SquareModuleDrawer,
    "gapped": GappedSquareModuleDrawer,
    "circle": CircleModuleDrawer,
    "rounded": RoundedModuleDrawer,
    "vertical-bars": VerticalBarsDrawer,
    "horizontal-bars": HorizontalBarsDrawer,
}


def _get_drawer(style: str):
    cls = _DRAWERS.get(style, SquareModuleDrawer)
    return cls()


def _generate_qr_image(url: str, size: int, style: str = "square", embed_image: bytes | None = None) -> tuple[Image.Image, int]:
    """Build a styled QR-code image (PIL ``Image``) at the requested pixel size.

    When *embed_image* is provided the error-correction level is raised to H
    and the image is centre-cropped to a square before being placed in the
    middle of the QR code.
    """
    error_correction = qrcode.constants.ERROR_CORRECT_H if embed_image else qrcode.constants.ERROR_CORRECT_M
    qr = qrcode.QRCode(border=2, error_correction=error_correction)
    qr.add_data(url)
    qr.make(fit=True)

    box_size = _auto_box_size(qr.modules_count, size)
    qr.border = 2
    qr.box_size = box_size
    qr.make(fit=True)

    drawer = _get_drawer(style)
    kw = dict(image_factory=StyledPilImage, module_drawer=drawer, color_mask=SolidFillColorMask())

    if embed_image:
        logo = Image.open(BytesIO(embed_image)).convert("RGBA")
        logo_size = min(logo.size)
        left = (logo.width - logo_size) // 2
        top = (logo.height - logo_size) // 2
        logo = logo.crop((left, top, left + logo_size, top + logo_size))
        buf = BytesIO()
        logo.save(buf, format="PNG")
        buf.seek(0)
        kw["embeded_image_path"] = buf

    img = qr.make_image(**kw).convert("L")
    img = img.resize((size, size), Image.LANCZOS)

    return img, size


def preview_qr_code(url: str, size: int, style: str = "square", embed_image: bytes | None = None) -> PreviewResponse:
    """Generate a preview PNG of the QR code without creating a print job."""
    img, size = _generate_qr_image(url, size, style, embed_image)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return PreviewResponse.from_preview_image(buf, size, size)


def print_qr_code(url: str, size: int, job_manager: JobManager, ble_device_name: str = "X5h-10B5", style: str = "square", embed_image: bytes | None = None):
    """Generate a QR code and enqueue it as a new print job.

    The QR-code image is centred on the printer-width canvas and nibble-encoded
    before being passed to ``job_manager.create_job``.
    """
    settings = _load_qr_settings()
    printer_width = settings.width
    size = max(50, min(printer_width, size))

    img, size = _generate_qr_image(url, size, style, embed_image)

    buf = BytesIO()
    img.save(buf, format="PNG")
    preview_image = buf.getvalue()

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
            "ble_device_name": ble_device_name,
            "quality": settings.quality,
            "speed": settings.speed,
            "energy": settings.energy,
            "chunk_rows": settings.chunk_rows,
            "chunk_delay": settings.chunk_delay,
            "feed": settings.feed,
        },
        preview_image=preview_image,
    )
