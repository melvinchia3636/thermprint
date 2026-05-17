"""CLI entry point for direct printer usage without the FastAPI server.

Usage:
    python -m thermal_printer image.png [--device X5h-10B5] [--preview]
"""

import argparse
import asyncio
import logging

from lib.thermal_printer.image_processor import process_image
from lib.thermal_printer.simulator import simulate_print
from lib.thermal_printer.device import PrinterDevice

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


async def main():
    parser = argparse.ArgumentParser(
        description="Print an image to a Bluetooth thermal printer (grayscale mode)"
    )
    parser.add_argument("image", help="path to the image file")
    parser.add_argument(
        "--device",
        default="X5h-10B5",
        help="BLE device name to search for (default: X5h-10B5)",
    )
    parser.add_argument(
        "--width", type=int, default=384, help="printer width in pixels (default: 384)"
    )
    parser.add_argument(
        "--quality",
        type=lambda x: int(x, 0),
        default=0x32,
        help="print quality 0x31-0x35 (default: 0x32)",
    )
    parser.add_argument(
        "--speed",
        type=lambda x: int(x, 0),
        default=0x10,
        help="feed speed, smaller=faster (default: 0x10)",
    )
    parser.add_argument(
        "--energy",
        type=lambda x: int(x, 0),
        default=0,
        help="thermal energy 0x0000-0xFFFF, 0=auto (default: 0)",
    )
    parser.add_argument(
        "--contrast", type=float, default=1.0, help="contrast multiplier (default: 1.0)"
    )
    parser.add_argument(
        "--gamma",
        type=float,
        default=1.0,
        help="gamma correction, higher=brighter (default: 1.0)",
    )
    parser.add_argument(
        "--chunk-rows", type=int, default=10, help="rows per data chunk (default: 10)"
    )
    parser.add_argument(
        "--chunk-delay",
        type=float,
        default=0.2,
        help="delay in seconds between chunks (default: 0.2)",
    )
    parser.add_argument(
        "--feed",
        type=int,
        default=200,
        help="paper feed pixels after print (default: 200)",
    )
    parser.add_argument(
        "--rotate",
        type=int,
        default=0,
        choices=[0, 90, 180, 270],
        help="rotate image (default: 0)",
    )
    parser.add_argument(
        "--preview",
        nargs="?",
        const="preview.png",
        default=None,
        help="simulate print and save as image (default: preview.png)",
    )
    args = parser.parse_args()

    logger.info("Processing: %s", args.image)
    nibble_data, width, height, dithered = process_image(
        args.image, args.width, args.contrast, args.gamma, args.rotate
    )

    if args.preview:
        simulate_print(dithered, width, height, args.preview)
        return

    device = PrinterDevice(args.device)
    await device.discover()
    if not device.address:
        return
    await device.connect()
    try:
        await device.print_data(
            nibble_data=nibble_data,
            width=width,
            quality=args.quality,
            speed=args.speed,
            energy=args.energy,
            chunk_rows=args.chunk_rows,
            chunk_delay=args.chunk_delay,
            feed=args.feed,
        )
    finally:
        await device.close()


if __name__ == "__main__":
    asyncio.run(main())
