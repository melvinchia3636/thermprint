import logging

from PIL import Image, ImageFilter, ImageEnhance

from thermal_printer.protocol import GRAY_LEVELS

logger = logging.getLogger(__name__)


def dither_gray_pixels(gray_pixels, width, height):
    buf = list(gray_pixels)
    step_in = 256 // GRAY_LEVELS
    step_out = 256 // (GRAY_LEVELS - 1)

    for y in range(height):
        has_below = y < height - 1
        for x in range(width):
            has_left = x > 0
            has_right = x < width - 1
            idx = y * width + x
            old_val = buf[idx]
            new_val = (old_val // step_in) * step_out
            buf[idx] = new_val
            error = old_val - new_val
            if has_right:
                buf[idx + 1] += (error * 7) // 16
            if has_left and has_below:
                buf[(y + 1) * width + (x - 1)] += (error * 3) // 16
            if has_below:
                buf[(y + 1) * width + x] += (error * 5) // 16
            if has_right and has_below:
                buf[(y + 1) * width + (x + 1)] += error // 16

    return buf


def gray_to_nibbles(gray_pixels, width, height):
    step_in = 256 // GRAY_LEVELS
    half_width = width // 2

    padding_rows = 16
    total_bytes = (height + padding_rows) * half_width
    if total_bytes % 4 != 0:
        total_bytes += total_bytes % 4
    result = bytearray(total_bytes)

    out_idx = padding_rows * half_width
    nibble_buf = []
    for val in gray_pixels:
        level_idx = val // step_in
        if level_idx >= GRAY_LEVELS:
            level_idx = GRAY_LEVELS - 1
        nibble = GRAY_LEVELS - 1 - level_idx
        nibble = max(0, min(15, nibble))
        nibble_buf.append(nibble)
        if len(nibble_buf) == 2:
            if out_idx < len(result):
                result[out_idx] = (nibble_buf[1] << 4) | nibble_buf[0]
                out_idx += 1
            nibble_buf = []

    return bytes(result)


def process_image(
    image_path,
    printer_width,
    contrast,
    gamma,
    rotate=0,
    threshold_scale=0.46,
    sharpness=1.1,
    low_threshold=0.2,
    high_threshold=0.2,
    low_value=110,
    high_value=150,
    gray_scale=1.0,
):
    img = Image.open(image_path)

    if img.mode == "RGBA":
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    if rotate != 0:
        img = img.rotate(rotate, expand=True)

    orig_width, orig_height = img.size
    new_height = int(orig_height * (printer_width / orig_width))
    img = img.resize((printer_width, new_height), Image.LANCZOS)

    if sharpness > 0:
        img = img.filter(
            ImageFilter.UnsharpMask(radius=2, percent=int(sharpness * 100), threshold=0)
        )

    gray = img.convert("L")
    pixels = list(gray.getdata())

    width, height = gray.size
    total = len(pixels)

    histogram = [0] * 256
    for p in pixels:
        histogram[p] += 1

    low_cumulative_target = int(total * low_threshold)
    high_cumulative_target = int(total * high_threshold)

    cumulative = 0
    low_percentile = 0
    for i in range(256):
        cumulative += histogram[i]
        if cumulative > low_cumulative_target:
            low_percentile = i
            break

    cumulative = 0
    high_percentile = 255
    for i in range(255, -1, -1):
        cumulative += histogram[i]
        if cumulative > high_cumulative_target:
            high_percentile = i
            break

    if low_percentile > low_value:
        low_percentile = low_value
    if high_percentile < high_value:
        high_percentile = high_value

    scale = threshold_scale
    low_mapped = low_percentile * scale
    high_mapped = high_percentile + (255 - high_percentile) * (1.0 - scale)
    mid_range = high_mapped - low_mapped
    mid_denom = (
        high_percentile - low_percentile if high_percentile != low_percentile else 1
    )

    for i in range(total):
        p = pixels[i]
        if p <= low_percentile:
            out = p * scale
        elif p >= high_percentile:
            out = p + (255 - p) * (1.0 - scale)
        else:
            ratio = (p - low_percentile) / mid_denom
            out = ratio * mid_range + low_mapped
        out = int(out * gray_scale)
        pixels[i] = max(0, min(255, out))

    if contrast != 1.0:
        pixels = [max(0, min(255, int((p - 128) * contrast + 128))) for p in pixels]
    if gamma != 1.0:
        inv_gamma = 1.0 / gamma
        pixels = [min(255, int(255.0 * ((p / 255.0) ** inv_gamma))) for p in pixels]

    pixels = [255 if p > 250 else (0 if p < 5 else p) for p in pixels]

    dithered = dither_gray_pixels(pixels, width, height)
    nibble_data = gray_to_nibbles(dithered, width, height)

    logger.info(
        "Image processed: %dx%d, low=%d high=%d, nibble data: %d bytes",
        width, height, low_percentile, high_percentile, len(nibble_data),
    )
    return nibble_data, width, height, dithered
