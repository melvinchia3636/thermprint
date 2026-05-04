from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    name: str | None = Field(description="BLE device name")
    address: str = Field(description="BLE device MAC address")


class DeviceListResponse(BaseModel):
    devices: list[DeviceInfo] = Field(description="List of discovered BLE devices")


class DeviceConfigResponse(BaseModel):
    ble_device_name: str = Field(description="Currently configured BLE printer name")
