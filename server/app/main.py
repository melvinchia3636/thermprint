import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.logging import ColourizedFormatter

from server.app.bootstrap import Settings
from server.app.services.printer.printer_service import PrinterManager
from server.app.services.jobs.job_manager import JobManager
from server.app.services.jobs.database import DatabaseService
from server.app.services.stores.settings_store import SettingsStore
from server.app.services.stores.device_store import DeviceStore
from server.app.error_handlers import validation_exception_handler
from server.app.routes.printer import print as print_routes
from server.app.routes.printer import preview as preview_routes
from server.app.routes.printer import qrcode as qrcode_routes
from server.app.routes.jobs import jobs as jobs_routes
from server.app.routes.device import device as device_routes
from server.app.routes.device import status as status_routes
from server.app.routes import ws
from server.app.routes import settings as settings_routes

_handler = logging.StreamHandler()
_handler.setFormatter(
    ColourizedFormatter("%(levelprefix)s %(message)s")
)
logging.basicConfig(level=logging.INFO, handlers=[_handler])
logger = logging.getLogger("thermal_printer")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    settings_store = SettingsStore()
    settings_store.load()
    device_store = DeviceStore()
    device_store.load()
    db = DatabaseService()
    await db.start()
    printer = PrinterManager()
    job_mgr = JobManager(printer, db)
    app.state.settings = settings
    app.state.settings_store = settings_store
    app.state.device_store = device_store
    app.state.printer_manager = printer
    app.state.job_manager = job_mgr
    job_mgr.start()
    stored = device_store.load()
    logger.info("Server started, BLE device: %s", stored.get("ble_device_name", "X5h-10B5"))
    yield
    await job_mgr.stop()
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

app.include_router(preview_routes.router)
app.include_router(print_routes.router)
app.include_router(jobs_routes.router)
app.include_router(device_routes.router)
app.include_router(status_routes.router)
app.include_router(ws.router)
app.include_router(settings_routes.router)
app.include_router(qrcode_routes.router)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
