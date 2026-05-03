import asyncio

from bleak import BleakScanner, BleakClient

from thermal_printer.protocol import (
    WRITE_UUID,
    set_quality,
    set_energy,
    set_print_mode_gray16,
    feed_paper_speed,
    feed_paper,
    get_dev_state,
    build_gray_scan_packet,
)


class PrinterDevice:
    def __init__(self, name_filter):
        self.name_filter = name_filter
        self.address = None
        self._client = None
        self.mtu_size = 23

    async def discover(self):
        print("\U0001f50d scanning...")
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name and self.name_filter in d.name:
                self.address = d.address
                print(f"\U0001f3af found: {d.name}")
                return
        print("\u274c device not found")

    async def connect(self):
        if not self.address:
            raise RuntimeError("No device address. Call discover() first.")
        self._client = BleakClient(self.address)
        await self._client.connect()
        print("\U0001f9e0 connected")
        self.mtu_size = self._client.mtu_size
        print(f"\U0001f4e1 MTU: {self.mtu_size}")

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

        print(
            f"\U0001f4e6 {len(chunks)} chunks (quality=0x{quality:02X} speed=0x{speed:02X})"
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
            print(f"  chunk {i + 1}/{len(chunks)} ({len(chunk)} \u2192 {len(pkt)} bytes)")

        await asyncio.sleep(1.0)
        await self.send(feed_paper(feed))
        await asyncio.sleep(0.3)
        await self.send(get_dev_state())
        await asyncio.sleep(0.1)

        print("\U0001f5a8\ufe0f DONE")

    async def close(self):
        if self._client:
            await self._client.disconnect()
            self._client = None
