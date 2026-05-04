import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from server.app.config import Settings
from server.app.services.printer_service import PrinterManager
from server.app.services.job_manager import JobManager
from server.app.services.settings_store import SettingsStore
from server.app.services.device_store import DeviceStore
from server.app.error_handlers import validation_exception_handler
from server.app.routes import preview, print, jobs, devices, status, ws, settings, qrcode, device

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    settings_store = SettingsStore()
    settings_store.load()
    device_store = DeviceStore()
    device_store.load()
    printer = PrinterManager()
    job_mgr = JobManager(printer)
    app.state.settings = settings
    app.state.settings_store = settings_store
    app.state.device_store = device_store
    app.state.printer_manager = printer
    app.state.job_manager = job_mgr
    job_mgr.start()
    stored = device_store.load()
    logger.info("Server started, BLE device: %s", stored.get("ble_device_name", "X5h-10B5"))
    yield
    job_mgr.stop()
    await printer.disconnect()


app = FastAPI(
    title="Thermal Printer API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(preview.router)
app.include_router(print.router)
app.include_router(jobs.router)
app.include_router(devices.router)
app.include_router(status.router)
app.include_router(ws.router)
app.include_router(settings.router)
app.include_router(qrcode.router)
app.include_router(device.router)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
