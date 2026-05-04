import asyncio
import logging
from enum import Enum

from bleak.exc import BleakError

from thermal_printer.device import PrinterDevice
from thermal_printer.protocol import (
    set_quality,
    set_energy,
    set_print_mode_gray16,
    feed_paper_speed,
    feed_paper,
    get_dev_state,
    build_gray_scan_packet,
)
from server.app.services.broadcast import BroadcastService

logger = logging.getLogger(__name__)


class ConnectionStatus(str, Enum):
    offline = "offline"
    connecting = "connecting"
    online = "online"


class PrinterManager:
    def __init__(self):
        self._device: PrinterDevice | None = None
        self._current_name_filter: str | None = None
        self._status: ConnectionStatus = ConnectionStatus.offline
        self._broadcast = BroadcastService()

    @property
    def status(self) -> ConnectionStatus:
        return self._status

    @status.setter
    def status(self, value: ConnectionStatus):
        self._status = value
        self._broadcast.publish(value.value)

    def subscribe_status(self) -> asyncio.Queue[str]:
        return self._broadcast.subscribe(self._status.value)

    def unsubscribe_status(self, q: asyncio.Queue[str]):
        self._broadcast.unsubscribe(q)

    async def ensure_connected(self, name_filter: str) -> PrinterDevice:
        if self._device is not None and self._current_name_filter == name_filter:
            try:
                await self._device.send(b"")
                self.status = ConnectionStatus.online
                return self._device
            except (BleakError, AttributeError, OSError):
                logger.warning("BLE connection lost, reconnecting...")
                await self.disconnect()
        await self.disconnect()
        self.status = ConnectionStatus.connecting
        device = PrinterDevice(name_filter)

        last_exc = None
        for attempt in range(5):
            try:
                await device.discover()
                if not device.address:
                    raise RuntimeError(f"Printer '{name_filter}' not found via BLE")
                try:
                    await device.connect()
                except BleakError as exc:
                    if "Service Discovery" in str(exc):
                        logger.warning(
                            "Service discovery failed on connect (attempt %d/5)...",
                            attempt + 1,
                        )
                        await asyncio.sleep(1)
                        await device.disconnect()
                        continue
                    raise
                self._device = device
                self._current_name_filter = name_filter
                self.status = ConnectionStatus.online
                return self._device
            except Exception as exc:
                last_exc = exc
                logger.warning("Connection attempt %d/5 failed: %s", attempt + 1, exc)
                await asyncio.sleep(1)
                continue

        self.status = ConnectionStatus.offline
        raise last_exc or RuntimeError(
            f"Could not connect to printer '{name_filter}' after 5 attempts"
        )

    async def print_job(
        self,
        nibble_data: bytes,
        width: int,
        quality: int,
        speed: int,
        energy: int,
        chunk_rows: int,
        chunk_delay: float,
        feed: int,
        ble_device_name: str = "X5h-10B5",
        progress_callback=None,
        cancel_event=None,
        connection_callback=None,
    ):
        for attempt in range(2):
            try:
                device = await self.ensure_connected(ble_device_name)
                if connection_callback:
                    connection_callback()
                half_width = width // 2
                chunk_size = half_width * chunk_rows

                chunks = []
                offset = 0
                while offset < len(nibble_data):
                    end = min(offset + chunk_size, len(nibble_data))
                    chunks.append(nibble_data[offset:end])
                    offset = end

                logger.info(
                    "Printing %d chunks (quality=0x%02X speed=0x%02X)",
                    len(chunks),
                    quality,
                    speed,
                )

                if cancel_event and cancel_event.is_set():
                    return

                await device.send(set_quality(quality))
                await asyncio.sleep(0.1)

                if energy > 0:
                    await device.send(set_energy(energy))
                    await asyncio.sleep(0.1)

                await device.send(set_print_mode_gray16())
                await asyncio.sleep(0.1)

                await device.send(feed_paper_speed(speed))
                await asyncio.sleep(0.2)

                for i, chunk in enumerate(chunks):
                    if cancel_event and cancel_event.is_set():
                        logger.info("Job cancelled mid-print after %d chunks", i)
                        return
                    pkt = build_gray_scan_packet(chunk)
                    await device.send(pkt)
                    await device.send(feed_paper_speed(speed))
                    await asyncio.sleep(chunk_delay)
                    if progress_callback:
                        progress_callback(i + 1, len(chunks))

                await asyncio.sleep(1.0)
                await device.send(feed_paper(feed))
                await asyncio.sleep(0.3)
                await device.send(get_dev_state())
                await asyncio.sleep(0.1)
                return
            except (BleakError, AttributeError, OSError) as exc:
                msg = str(exc)
                logger.warning("Print attempt %d failed: %s", attempt + 1, msg)
                await self.disconnect()
                if attempt == 0 and (
                    "Service Discovery" in msg or "discovery" in msg.lower()
                ):
                    logger.info("Retrying after service discovery failure...")
                    await asyncio.sleep(1)
                    continue
                raise

    async def disconnect(self):
        if self._device:
            try:
                await self._device.close()
            except Exception:
                pass
            self._device = None
            self._current_name_filter = None
        self.status = ConnectionStatus.offline
