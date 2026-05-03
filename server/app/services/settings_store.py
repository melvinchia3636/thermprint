import json
import logging
import os
from pathlib import Path

from server.app.schemas.print_settings import PrintSettings

logger = logging.getLogger(__name__)

_SETTINGS_PATH = Path(__file__).resolve().parent.parent.parent / "settings.json"


class SettingsStore:
    def __init__(self, path: str | None = None):
        self._path = Path(path) if path else _SETTINGS_PATH
        self._data: dict = {}

    def load(self) -> PrintSettings:
        if not self._path.exists():
            logger.info("Settings file not found at %s, using defaults", self._path)
            self._data = PrintSettings().model_dump()
            self._save()
            return PrintSettings()
        try:
            with open(self._path) as f:
                self._data = json.load(f)
            return PrintSettings(**self._data)
        except (json.JSONDecodeError, OSError, Exception) as exc:
            logger.warning("Failed to load settings: %s, using defaults", exc)
            self._data = PrintSettings().model_dump()
            return PrintSettings()

    def save(self, settings: PrintSettings) -> PrintSettings:
        self._data = settings.model_dump()

        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._path, "w") as f:
                json.dump(self._data, f, indent=2)
            logger.info("Settings saved to %s", self._path)
        except OSError as exc:
            logger.error("Failed to save settings: %s", exc)

        return settings
