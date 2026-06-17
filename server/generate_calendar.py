"""Generate a monthly calendar image for the thermal printer.

Usage:
    python generate_calendar.py [output_path]

Creates a 384px-wide monochrome calendar image for the current month and year.
If no output path is given, saves to ``calendar.png`` in the current directory.
"""

import calendar
import datetime
import os
import sys

from PIL import Image, ImageDraw, ImageFont

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


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Return a TrueType font at *size* pt, falling back to Pillow's default."""
    if bold:
        paths = [
            ("/System/Library/Fonts/Helvetica.ttc", 1),
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", None),
            ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", None),
        ]
    else:
        paths = [
            ("/System/Library/Fonts/Helvetica.ttc", None),
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", None),
            ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", None),
        ]
    for path, index in paths:
        if os.path.exists(path):
            kwargs = {"size": size}
            if index is not None:
                kwargs["index"] = index
            return ImageFont.truetype(path, **kwargs)
    return ImageFont.load_default()


def generate_calendar(year: int, month: int) -> Image.Image:
    """Build a 384 px wide monochrome calendar image for the given month."""
    cal = calendar.Calendar(firstweekday=0)
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
    month_name = calendar.month_name[month]
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


def main() -> None:
    now = datetime.datetime.now()
    img = generate_calendar(now.year, now.month)

    output = sys.argv[1] if len(sys.argv) > 1 else "calendar.png"
    img.save(output, format="PNG")
    print(f"Calendar saved to {output} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()
