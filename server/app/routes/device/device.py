"""Device-related endpoints.

* ``GET  /api/device`` — return the currently configured BLE device name
* ``PUT  /api/device`` — persist a new BLE device name
* ``GET  /api/devices`` — scan for nearby BLE printers
"""

from fastapi import APIRouter, Depends, Request
from bleak import BleakScanner

from server.app.services.stores.device_store import DeviceStore
from server.app.schemas.device import DeviceInfo, DeviceListResponse, DeviceConfigResponse

router = APIRouter(prefix="/api", tags=["Device"])


def _get_device_store(request: Request) -> DeviceStore:
    return request.app.state.device_store


@router.get("/devices", response_model=DeviceListResponse)
async def list_devices():
    """Scan for nearby BLE printers (5-second timeout)."""
    found = await BleakScanner.discover(timeout=5)
    return DeviceListResponse(
        devices=[DeviceInfo(name=d.name, address=d.address) for d in found if d.name]
    )


@router.get("/device", response_model=DeviceConfigResponse)
async def get_device(
    store: DeviceStore = Depends(_get_device_store),
):
    """Return the currently configured BLE printer name."""
    return DeviceConfigResponse(**store.load())


@router.put("/device", response_model=DeviceConfigResponse)
async def update_device(
    body: DeviceConfigResponse,
    store: DeviceStore = Depends(_get_device_store),
):
    """Persist a new BLE printer name."""
    return DeviceConfigResponse(**store.save(body.ble_device_name))
