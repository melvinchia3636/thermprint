import asyncio
import logging

from bleak import BleakScanner, BleakClient

from lib.thermal_printer.protocol import (
    WRITE_UUID,
    set_quality,
    set_energy,
    set_print_mode_gray16,
    feed_paper_speed,
    feed_paper,
    get_dev_state,
    build_gray_scan_packet,
)

logger = logging.getLogger(__name__)


class PrinterDevice:
    def __init__(self, name_filter):
        self.name_filter = name_filter
        self.address = None
        self._client = None
        self.mtu_size = 23

    async def discover(self):
        logger.info("Scanning for BLE device: %s", self.name_filter)
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name and self.name_filter in d.name:
                self.address = d.address
                logger.info("Found BLE device: %s", d.name)
                return
        logger.warning("BLE device not found: %s", self.name_filter)

    async def connect(self):
        if not self.address:
            raise RuntimeError("No device address. Call discover() first.")
        self._client = BleakClient(self.address)
        await self._client.connect()
        logger.info("Connected to BLE device (MTU: %d)", self._client.mtu_size)
        self.mtu_size = self._client.mtu_size

    async def send(self, data):
        for i in range(0, len(data), self.mtu_size - 3):
            chunk = data[i : i + self.mtu_size - 3]
            await self._client.write_gatt_char(WRITE_UUID, chunk, response=False)
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.02)

    async def print_data(
        self,
        nibble_data,
        width,
        quality,
        speed,
        energy,
        chunk_rows,
        chunk_delay,
        feed,
    ):
        half_width = width // 2
        chunk_size = half_width * chunk_rows

        chunks = []
        offset = 0
        while offset < len(nibble_data):
            end = min(offset + chunk_size, len(nibble_data))
            chunks.append(nibble_data[offset:end])
            offset = end

        logger.info(
            "Sending %d chunks (quality=0x%02X speed=0x%02X)", len(chunks), quality, speed
        )

        await self.send(set_quality(quality))
        await asyncio.sleep(0.1)

        if energy > 0:
            await self.send(set_energy(energy))
            await asyncio.sleep(0.1)

        await self.send(set_print_mode_gray16())
        await asyncio.sleep(0.1)

        await self.send(feed_paper_speed(speed))
        await asyncio.sleep(0.2)

        for i, chunk in enumerate(chunks):
            pkt = build_gray_scan_packet(chunk)
            await self.send(pkt)
            await self.send(feed_paper_speed(speed))
            await asyncio.sleep(chunk_delay)
            logger.debug(
                "Chunk %d/%d (%d bytes)", i + 1, len(chunks), len(chunk)
            )

        await asyncio.sleep(1.0)
        await self.send(feed_paper(feed))
        await asyncio.sleep(0.3)
        await self.send(get_dev_state())
        await asyncio.sleep(0.1)

        logger.info("Print job completed")

    async def close(self):
        if self._client:
            await self._client.disconnect()
            self._client = None
