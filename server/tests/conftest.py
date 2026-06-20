import asyncio
import json
import tempfile
from enum import Enum
from io import BytesIO
from pathlib import Path

import pytest
import pytest_asyncio
from PIL import Image
from fastapi import FastAPI
from fastapi.testclient import TestClient

from server.app.bootstrap import Settings
from server.app.schemas.print_settings import PrintSettings
from server.app.services.jobs.database import DatabaseService
from server.app.services.jobs.job_manager import JobManager
from server.app.services.stores.device_store import DeviceStore
from server.app.services.stores.settings_store import SettingsStore
from server.app.routes.printer import preview, print as print_route, qrcode, calendar as calendar_route
from server.app.routes.jobs import jobs as jobs_route
from server.app.routes.device import device as device_route, status as status_route
from server.app.routes import settings as settings_route, ws
from server.app.error_handlers import validation_exception_handler
from fastapi.exceptions import RequestValidationError


def _make_test_image(size=(100, 80)) -> bytes:
    img = Image.new("RGB", size, (200, 100, 50))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class FakePrinterManager:
    """Stand-in for PrinterManager that does nothing."""

    class _ConnectionStatus(str, Enum):
        offline = "offline"
        connecting = "connecting"
        online = "online"

    def __init__(self):
        self._status: FakePrinterManager._ConnectionStatus = self._ConnectionStatus.offline

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    async def ensure_connected(self, name_filter: str):
        pass

    async def print_job(self, **kwargs):
        pass

    async def disconnect(self):
        pass

    def subscribe_status(self):
        q: asyncio.Queue = asyncio.Queue()
        q.put_nowait(self._status)
        return q

    def unsubscribe_status(self, q):
        pass


@pytest.fixture
def settings_file():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        json.dump(PrintSettings().model_dump(), f)
        tmp = f.name
    yield tmp
    Path(tmp).unlink(missing_ok=True)


@pytest.fixture
def device_file():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        json.dump({"ble_device_name": "X5h-10B5"}, f)
        tmp = f.name
    yield tmp
    Path(tmp).unlink(missing_ok=True)


@pytest_asyncio.fixture
async def app(settings_file, device_file):
    app = FastAPI()
    settings_store = SettingsStore(settings_file)
    settings_store.load()
    device_store = DeviceStore(device_file)
    device_store.load()
    db = DatabaseService(":memory:")
    await db.start()
    printer = FakePrinterManager()
    job_mgr = JobManager(printer, db)
    job_mgr.start()
    app.state.settings = Settings()
    app.state.settings_store = settings_store
    app.state.device_store = device_store
    app.state.printer_manager = printer
    app.state.job_manager = job_mgr
    app.include_router(preview.router)
    app.include_router(print_route.router)
    app.include_router(jobs_route.router)
    app.include_router(qrcode.router)
    app.include_router(calendar_route.router)
    app.include_router(device_route.router)
    app.include_router(status_route.router)
    app.include_router(settings_route.router)
    app.include_router(ws.router)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    yield app
    await job_mgr.stop()
    await db.stop()


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_image():
    return _make_test_image()
