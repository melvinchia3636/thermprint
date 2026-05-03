from pydantic import BaseModel, Field


class PrintSettings(BaseModel):
    ble_device_name: str = Field(default="X5h-10B5", description="BLE device name filter")
    width: int = Field(default=384, ge=64, le=1000, description="Printer width in pixels")
    quality: int = Field(default=0x32, ge=0x31, le=0x35, description="Print quality")
    speed: int = Field(default=0x10, ge=0x01, le=0xFF, description="Feed speed, smaller=faster")
    energy: int = Field(default=0, ge=0, le=65535, description="Thermal energy, 0=auto")
    contrast: float = Field(default=1.0, ge=0.0, le=5.0, description="Contrast multiplier")
    gamma: float = Field(default=1.0, ge=0.1, le=5.0, description="Gamma correction, higher=brighter")
    rotate: int = Field(default=0, ge=0, le=270, description="Image rotation degrees")
    chunk_rows: int = Field(default=10, ge=1, le=100, description="Rows per data chunk")
    chunk_delay: float = Field(default=0.2, ge=0.0, le=10.0, description="Delay in seconds between chunks")
    feed: int = Field(default=200, ge=0, le=5000, description="Paper feed pixels after print")
