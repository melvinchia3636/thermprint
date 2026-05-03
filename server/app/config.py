from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "THERMAL_"}
    max_upload_size_mb: int = 10
