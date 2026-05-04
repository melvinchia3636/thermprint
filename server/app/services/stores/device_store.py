"""Persistent storage for the selected BLE printer device name."""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_DEVICE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "device.json"


class DeviceStore:
    """Reads and writes the printer BLE device name to a JSON file on disk."""

    def __init__(self):
        self._data: dict = {}

    def load(self) -> dict:
        """Load the saved device name from disk. Falls back to a default on failure."""
        try:
            with open(_DEVICE_PATH) as f:
                self._data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load device config: %s, using defaults", exc)
            self._data = {"ble_device_name": "X5h-10B5"}
            self._save()
        return dict(self._data)

    def _save(self):
        """Write the current in-memory data to the JSON file."""
        try:
            _DEVICE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(_DEVICE_PATH, "w") as f:
                json.dump(self._data, f, indent=2)
        except OSError as exc:
            logger.error("Failed to save device config: %s", exc)

    def save(self, ble_device_name: str) -> dict:
        """Persist a new BLE device name to disk."""
        self._data = {"ble_device_name": ble_device_name}
        self._save()
        return dict(self._data)
