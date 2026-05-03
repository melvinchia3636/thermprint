from io import BytesIO

from PIL import Image

from thermal_printer.protocol import GRAY_LEVELS


def simulate_print(dithered_pixels, width, height, output):
    step_in = 256 // GRAY_LEVELS
    thermal_gamma = 1.6
    preview = Image.new("L", (width, height))
    out_pixels = []
    for val in dithered_pixels:
        level_idx = val // step_in
        if level_idx >= GRAY_LEVELS:
            level_idx = GRAY_LEVELS - 1
        nibble = GRAY_LEVELS - 1 - level_idx
        nibble = max(0, min(15, nibble))
        gray_out = 255 - (nibble * 255 // 15)
        gray_out = int(255 * ((gray_out / 255.0) ** thermal_gamma))
        out_pixels.append(gray_out)
    preview.putdata(out_pixels)
    preview.save(output, format="PNG")
    if isinstance(output, BytesIO):
        output.seek(0)
    else:
        print(f"\U0001f5bc\ufe0f preview saved: {output}")
