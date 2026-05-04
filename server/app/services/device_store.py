import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_DEVICE_PATH = Path(__file__).resolve().parent.parent / "configs" / "device.json"


class DeviceStore:
    def __init__(self):
        self._data: dict = {}

    def load(self) -> dict:
        try:
            with open(_DEVICE_PATH) as f:
                self._data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load device config: %s, using defaults", exc)
            self._data = {"ble_device_name": "X5h-10B5"}
        return dict(self._data)

    def save(self, ble_device_name: str) -> dict:
        self._data = {"ble_device_name": ble_device_name}
        try:
            _DEVICE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(_DEVICE_PATH, "w") as f:
                json.dump(self._data, f, indent=2)
        except OSError as exc:
            logger.error("Failed to save device config: %s", exc)
        return dict(self._data)
