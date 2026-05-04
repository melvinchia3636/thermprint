from fastapi import APIRouter, Depends, Request

from server.app.schemas.print_settings import PrintSettings
from server.app.services.settings_store import SettingsStore

router = APIRouter(prefix="/api", tags=["Settings"])


def _get_settings_store(request: Request) -> SettingsStore:
    return request.app.state.settings_store


@router.get("/settings", response_model=PrintSettings)
async def get_settings(
    store: SettingsStore = Depends(_get_settings_store),
):
    return store.load()


@router.put("/settings", response_model=PrintSettings)
async def update_settings(
    settings: PrintSettings,
    store: SettingsStore = Depends(_get_settings_store),
):
    return store.save(settings)
