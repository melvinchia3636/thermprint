from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class JobStatus(str, Enum):
    queued = "queued"
    connecting = "connecting"
    printing = "printing"
    done = "done"
    failed = "failed"
    cancelled = "cancelled"


class JobType(str, Enum):
    image = "image"
    qr_code = "qr_code"


class PrintResponse(BaseModel):
    job_id: str = Field(description="Unique job identifier")
    status: JobStatus = Field(description="Initial job status")


class JobStatusResponse(BaseModel):
    job_id: str = Field(description="Unique job identifier")
    type: JobType = Field(description="Job type")
    status: JobStatus = Field(description="Current job status")
    progress: str | None = Field(default=None, description="Progress description, e.g. '3/10 chunks'")
    error: str | None = Field(default=None, description="Error message if failed")
    created_at: datetime = Field(description="Job creation timestamp")


class JobListResponse(BaseModel):
    jobs: list[JobStatusResponse] = Field(description="List of jobs, newest first")


class QRCodeRequest(BaseModel):
    url: HttpUrl = Field(description="URL to encode as QR code")
    size: int = Field(default=384, ge=50, le=384, description="QR code size in pixels")
    style: str = Field(default="square", description="QR code module style")
