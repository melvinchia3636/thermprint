from fastapi import Form

from server.app.schemas.print_settings import PrintSettings


def parse_print_settings(
    width: int = Form(384),
    quality: int = Form(0x32),
    speed: int = Form(0x10),
    energy: int = Form(0),
    contrast: float = Form(1.0),
    gamma: float = Form(1.0),
    rotate: int = Form(0),
    chunk_rows: int = Form(10),
    chunk_delay: float = Form(0.2),
    feed: int = Form(200),
    split_cols: int = Form(1, ge=1, le=10),
    split_rows: int = Form(1, ge=1, le=10),
) -> PrintSettings:
    return PrintSettings(
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
        split_cols=split_cols,
        split_rows=split_rows,
    )
