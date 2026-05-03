import tempfile
from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image
from fastapi import FastAPI
from fastapi.testclient import TestClient

from server.app.config import Settings
from server.app.schemas.print_settings import PrintSettings
from server.app.services.settings_store import SettingsStore
from server.app.routes import preview, print, jobs


def _make_test_image(size=(100, 80)) -> bytes:
    img = Image.new("RGB", size, (200, 100, 50))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class FakePrinterManager:
    async def ensure_connected(self, name_filter: str):
        pass

    async def print_job(self, **kwargs):
        pass

    async def disconnect(self):
        pass


@pytest.fixture
def settings_file():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        import json
        json.dump(PrintSettings().model_dump(), f)
        tmp = f.name
    yield tmp
    Path(tmp).unlink(missing_ok=True)


@pytest.fixture
def app(settings_file):
    app = FastAPI()
    settings_store = SettingsStore(settings_file)
    printer = FakePrinterManager()
    from server.app.services.job_manager import JobManager
    job_mgr = JobManager(printer)
    job_mgr.start()
    app.state.settings = Settings()
    app.state.settings_store = settings_store
    app.state.printer_manager = printer
    app.state.job_manager = job_mgr
    app.include_router(preview.router)
    app.include_router(print.router)
    app.include_router(jobs.router)
    yield app
    import asyncio
    asyncio.get_event_loop().run_until_complete(job_mgr.stop())


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_image():
    return _make_test_image()
