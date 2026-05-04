from fastapi import File

from server.app.schemas.print_settings import PrintSettings


def parse_print_settings(
    ble_device_name: str = File("X5h-10B5"),
    width: int = File(384),
    quality: int = File(0x32),
    speed: int = File(0x10),
    energy: int = File(0),
    contrast: float = File(1.0),
    gamma: float = File(1.0),
    rotate: int = File(0),
    chunk_rows: int = File(10),
    chunk_delay: float = File(0.2),
    feed: int = File(200),
) -> PrintSettings:
    return PrintSettings(
        ble_device_name=ble_device_name,
        width=width,
        quality=quality,
        speed=speed,
        energy=energy,
        contrast=contrast,
        gamma=gamma,
        rotate=rotate,
        chunk_rows=chunk_rows,
        chunk_delay=chunk_delay,
        feed=feed,
    )
