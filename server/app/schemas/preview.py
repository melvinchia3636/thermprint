import base64
from io import BytesIO

from pydantic import BaseModel, Field


class PreviewResponse(BaseModel):
    preview_url: str = Field(description="Base64 data URL of the preview PNG")
    width: int = Field(description="Processed image width")
    height: int = Field(description="Processed image height")

    @staticmethod
    def from_preview_image(buf: BytesIO, width: int, height: int) -> "PreviewResponse":
        encoded = base64.b64encode(buf.getvalue()).decode()
        return PreviewResponse(
            preview_url=f"data:image/png;base64,{encoded}",
            width=width,
            height=height,
        )
