"""Monthly calendar print-job creation.

Generates a monochrome calendar image for the given year and month, converts it
to printer nibble data, and creates a print job.  Also provides a standalone
preview function used by the ``POST /api/calendar/preview`` endpoint.
"""

import calendar as cal_mod
import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from lib.thermal_printer.image_processor import gray_to_nibbles
from server.app.schemas.preview import PreviewResponse
from server.app.services.jobs.job_manager import JobManager, JobType

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

WIDTH = 384
CELL_W = WIDTH // 7
MARGIN_LEFT = (WIDTH - CELL_W * 7) // 2

HEADER_H = 48
DAY_LABEL_H = 36
DAY_GAP = 10
CELL_H = 44
BOTTOM_PAD = 20
LINE_Y_OFFSET = 4

_CALENDAR_SETTINGS = {
    "width": WIDTH,
    "quality": 51,
    "speed": 20,
    "energy": 5000,
    "chunk_rows": 20,
    "chunk_delay": 0.15,
    "feed": 100,
}


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = [
        ("/System/Library/Fonts/Helvetica.ttc", 1 if bold else None),
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            None,
        ),
        (
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            None,
        ),
    ]
    for path, index in paths:
        if os.path.exists(path):
            kwargs = {"size": size}
            if index is not None:
                kwargs["index"] = index
            return ImageFont.truetype(path, **kwargs)
    return ImageFont.load_default()


def _generate_calendar_image(year: int, month: int) -> Image.Image:
    """Build a 384 px wide monochrome calendar image for the given month."""
    cal = cal_mod.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)

    rows = len(weeks)
    height = HEADER_H + DAY_LABEL_H + DAY_GAP + CELL_H * rows + BOTTOM_PAD

    img = Image.new("L", (WIDTH, height), 255)
    draw = ImageDraw.Draw(img)

    font_header = _get_font(26)
    font_label = _get_font(15)
    font_label_bold = _get_font(15, bold=True)
    font_day = _get_font(18)

    # ---------- header ----------
    month_name = cal_mod.month_name[month]
    header = f"{month_name} {year}"
    bbox = draw.textbbox((0, 0), header, font=font_header)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 8), header, fill=0, font=font_header)

    grid_right = MARGIN_LEFT + CELL_W * 7
    y_line = HEADER_H - LINE_Y_OFFSET
    draw.line([(MARGIN_LEFT, y_line), (grid_right, y_line)], fill=0, width=1)

    # ---------- day-of-week labels ----------
    label_top = HEADER_H - LINE_Y_OFFSET
    label_bottom = HEADER_H + DAY_LABEL_H - LINE_Y_OFFSET
    lbl_bbox = draw.textbbox((0, 0), "Ag", font=font_label)
    lbl_th = lbl_bbox[3] - lbl_bbox[1]
    y_label = label_top + ((label_bottom - label_top) - lbl_th) // 2

    for i, day in enumerate(DAYS):
        x = MARGIN_LEFT + i * CELL_W
        font = font_label_bold if day == "Sun" else font_label
        bbox = draw.textbbox((0, 0), day, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL_W - tw) // 2, y_label), day, fill=0, font=font)

    draw.line([(MARGIN_LEFT, label_bottom), (grid_right, label_bottom)], fill=0, width=1)

    # ---------- day numbers ----------
    for row_idx, week in enumerate(weeks):
        cell_top = HEADER_H + DAY_LABEL_H + DAY_GAP + row_idx * CELL_H
        for col_idx, day in enumerate(week):
            if day == 0:
                continue
            x = MARGIN_LEFT + col_idx * CELL_W
            day_str = str(day)
            bbox = draw.textbbox((0, 0), day_str, font=font_day)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            y = cell_top + (CELL_H - th) // 2
            draw.text((x + (CELL_W - tw) // 2, y), day_str, fill=0, font=font_day)

    return img


def preview_calendar(year: int, month: int) -> PreviewResponse:
    """Generate a preview PNG of the calendar without creating a print job."""
    img = _generate_calendar_image(year, month)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return PreviewResponse.from_preview_image(buf, img.width, img.height)


def print_calendar(
    year: int,
    month: int,
    job_manager: JobManager,
    ble_device_name: str = "X5h-10B5",
):
    """Generate a calendar image and enqueue it as a new print job."""
    settings = _CALENDAR_SETTINGS

    img = _generate_calendar_image(year, month)
    cal_width = img.width
    cal_height = img.height

    buf = BytesIO()
    img.save(buf, format="PNG")
    preview_image = buf.getvalue()

    pixels = list(img.getdata())
    nibble_data = gray_to_nibbles(pixels, cal_width, cal_height)

    return job_manager.create_job(
        JobType.calendar,
        nibble_data=nibble_data,
        width=cal_width,
        settings={
            "ble_device_name": ble_device_name,
            "quality": settings["quality"],
            "speed": settings["speed"],
            "energy": settings["energy"],
            "chunk_rows": settings["chunk_rows"],
            "chunk_delay": settings["chunk_delay"],
            "feed": settings["feed"],
        },
        preview_image=preview_image,
    )
