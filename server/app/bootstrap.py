from pydantic_settings import BaseSettings

from fastapi import Request


class Settings(BaseSettings):
    model_config = {"env_prefix": "THERMAL_"}
    max_upload_size_mb: int = 10


def get_job_manager(request: Request):
    return request.app.state.job_manager


def get_job_manager_ws(websocket):
    return websocket.app.state.job_manager


def get_device_name(request: Request) -> str:
    return request.app.state.device_store.load().get("ble_device_name", "X5h-10B5")

