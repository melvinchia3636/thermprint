"""Persistent storage for the printable-image print settings."""

import json
import logging
from pathlib import Path

from server.app.schemas.print_settings import PrintSettings

logger = logging.getLogger(__name__)

_SETTINGS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "image.json"


class SettingsStore:
    """Reads and writes image print settings (quality, speed, etc.) to a JSON file on disk."""

    def __init__(self, path: str | None = None):
        self._path = Path(path) if path else _SETTINGS_PATH
        self._data: dict = {}

    def _save(self):
        """Write the current in-memory data to the JSON file."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._path, "w") as f:
                json.dump(self._data, f, indent=2)
        except OSError as exc:
            logger.error("Failed to save settings: %s", exc)

    def load(self) -> PrintSettings:
        """Load settings from disk. Creates file with defaults if missing."""
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
        """Persist new print settings to disk."""
        self._data = settings.model_dump()
        self._save()
        return settings
