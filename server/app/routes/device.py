from fastapi import APIRouter, Depends, Request

from server.app.services.device_store import DeviceStore

router = APIRouter(prefix="/api", tags=["Device"])


def _get_device_store(request: Request) -> DeviceStore:
    return request.app.state.device_store


@router.get("/device", response_model=dict)
async def get_device(
    store: DeviceStore = Depends(_get_device_store),
):
    return store.load()


@router.put("/device", response_model=dict)
async def update_device(
    body: dict,
    store: DeviceStore = Depends(_get_device_store),
):
    return store.save(body.get("ble_device_name", "X5h-10B5"))
