from fastapi import Request

from server.app.config import Settings
from server.app.services.printer_service import PrinterManager
from server.app.services.job_manager import JobManager


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_printer_manager(request: Request) -> PrinterManager:
    return request.app.state.printer_manager


def get_job_manager(request: Request) -> JobManager:
    return request.app.state.job_manager
