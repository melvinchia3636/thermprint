from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    queued = "queued"
    printing = "printing"
    done = "done"
    failed = "failed"


class PrintResponse(BaseModel):
    job_id: str = Field(description="Unique job identifier")
    status: JobStatus = Field(description="Initial job status")


class JobStatusResponse(BaseModel):
    job_id: str = Field(description="Unique job identifier")
    status: JobStatus = Field(description="Current job status")
    progress: str | None = Field(default=None, description="Progress description, e.g. '3/10 chunks'")
    error: str | None = Field(default=None, description="Error message if failed")
    created_at: datetime = Field(description="Job creation timestamp")


class JobListResponse(BaseModel):
    jobs: list[JobStatusResponse] = Field(description="List of jobs, newest first")
