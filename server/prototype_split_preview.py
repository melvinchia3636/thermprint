"""Preview an image processed for thermal printing, overlaid with split grid lines.

Usage:
    python prototype_split_preview.py <image_path> <cols> <rows> [output_prefix]

Example:
    python prototype_split_preview.py photo.jpg 2 3

    Processes the image through the full thermal-printer pipeline and produces:
    - ``split_preview.png`` — dithered image with red dashed split-grid overlay
    - ``split_preview_to_be_printed.png`` — cells stacked vertically in reading
      order (left→right, top→bottom) as a long receipt strip, with white dashed
      separators between each chunk
    - Individual cell images (``split_preview_r0_c0.png``, etc.)
"""

import os
import sys
from io import BytesIO

from PIL import Image, ImageDraw

from lib.thermal_printer.image_processor import process_image
from lib.thermal_printer.simulator import simulate_print

PRINTER_WIDTH = 384
DASH_GAP = 8
DASH_LENGTH = 8


def _draw_split_lines(img: Image.Image, cols: int, rows: int) -> Image.Image:
    """Draw dashed red split-grid lines on a copy of the image."""
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

    return annotated


def _save_cells(img: Image.Image, cols: int, rows: int, prefix: str) -> None:
    """Extract each grid cell and save as a separate PNG."""
    w, h = img.size
    cell_w = w // cols
    cell_h = h // rows

    for r in range(rows):
        for c in range(cols):
            left = c * cell_w
            top = r * cell_h
            right = left + cell_w
            bottom = top + cell_h
            cell = img.crop((left, top, right, bottom))
            cell.save(f"{prefix}_r{r}_c{c}.png", format="PNG")


def _build_print_strip(img: Image.Image, cols: int, rows: int, output: str) -> None:
    """Stack cells vertically in reading order with white dashed separators."""
    w, h = img.size
    cell_w = w // cols
    cell_h = h // rows

    total = cols * rows
    canvas_h = total * cell_h

    canvas = Image.new("L", (PRINTER_WIDTH, canvas_h), 255)
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
        for x in range(0, PRINTER_WIDTH, DASH_GAP * 2):
            draw.line(
                [(x, sep_y), (x + DASH_LENGTH, sep_y)],
                fill=255,
                width=1,
            )

    canvas.save(output, format="PNG")
    print(f"\nTo-be-printed strip saved to: {output} ({PRINTER_WIDTH}×{canvas_h})")


def main() -> None:
    if len(sys.argv) < 4:
        print(
            "Usage: python prototype_split_preview.py <image_path> <cols> <rows> [output_prefix]",
            file=sys.stderr,
        )
        sys.exit(1)

    image_path = sys.argv[1]
    cols = int(sys.argv[2])
    rows = int(sys.argv[3])
    prefix = sys.argv[4] if len(sys.argv) > 4 else "split_preview"

    if not os.path.exists(image_path):
        print(f"File not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    if cols < 1 or rows < 1:
        print("cols and rows must be >= 1", file=sys.stderr)
        sys.exit(1)

    full_width = cols * PRINTER_WIDTH

    print(f"Processing {os.path.basename(image_path)} → {cols}×{rows} grid ({full_width}px wide)...")

    # ---- full pipeline (split) ----
    nb_split, w_split, h_split, dithered = process_image(
        image_path,
        printer_width=full_width,
        contrast=1.0,
        gamma=1.0,
    )

    # ---- full pipeline (unsplit / single-strip) ----
    _, w_single, h_single, _ = process_image(
        image_path,
        printer_width=PRINTER_WIDTH,
        contrast=1.0,
        gamma=1.0,
    )

    # ---- preview image ----
    buf = BytesIO()
    simulate_print(dithered, w_split, h_split, buf)
    preview = Image.open(buf)

    # ---- overlay split lines ----
    annotated = _draw_split_lines(preview, cols, rows)
    preview_path = f"{prefix}.png"
    annotated.save(preview_path, format="PNG")
    print(f"\nAnnotated preview saved to: {preview_path} ({w_split}×{h_split})")

    # ---- scale comparison ----
    print(f"\n{'Scale comparison':─^45}")
    print(f"  Unsplitted (1×1)  →  {w_single:>5d} × {h_single:<5d} px  (1 strip)")
    print(f"  Splitted  ({cols}×{rows})  →  {w_split:>5d} × {h_split:<5d} px  ({cols * rows} strips)")
    print(f"  Width  scale factor:  ×{w_split / w_single:.1f}")
    print(f"  Height scale factor:  ×{h_split / h_single:.1f}")
    print(f"  Image area ratio:     ×{cols * rows}")

    # ---- individual cells ----
    print(f"\n{'Cell slices'} {'─'*32}")
    print(f"  Each cell: {w_split // cols} × {h_split // rows} px")
    _save_cells(preview, cols, rows, prefix)

    # ---- to-be-printed long strip ----
    _build_print_strip(preview, cols, rows, f"{prefix}_to_be_printed.png")


if __name__ == "__main__":
    main()
