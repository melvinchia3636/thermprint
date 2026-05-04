from unittest.mock import patch


class TestDeviceEndpoint:
    def test_get_device_returns_default(self, client):
        resp = client.get("/api/device")
        assert resp.status_code == 200
        assert resp.json()["ble_device_name"] == "X5h-10B5"

    def test_put_device_updates_name(self, client):
        resp = client.put(
            "/api/device",
            json={"ble_device_name": "MyPrinter"},
        )
        assert resp.status_code == 200
        assert resp.json()["ble_device_name"] == "MyPrinter"

        get_resp = client.get("/api/device")
        assert get_resp.json()["ble_device_name"] == "MyPrinter"

    @patch("server.app.routes.device.device.BleakScanner.discover")
    def test_list_devices(self, mock_discover, client):
        mock_device = type("MockDevice", (), {
            "name": "Printer1",
            "address": "AA:BB:CC:DD:EE:FF",
        })
        mock_discover.return_value = [mock_device]

        resp = client.get("/api/devices")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["devices"]) == 1
        assert data["devices"][0]["name"] == "Printer1"
        assert data["devices"][0]["address"] == "AA:BB:CC:DD:EE:FF"
