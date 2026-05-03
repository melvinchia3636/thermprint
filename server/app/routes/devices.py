from fastapi import APIRouter
from bleak import BleakScanner

from server.app.schemas.devices import DeviceInfo, DeviceListResponse

router = APIRouter(prefix="/api", tags=["Devices"])


@router.get("/devices", response_model=DeviceListResponse)
async def list_devices():
    devices = await BleakScanner.discover(timeout=5)
    return DeviceListResponse(
        devices=[DeviceInfo(name=d.name, address=d.address) for d in devices if d.name]
    )
