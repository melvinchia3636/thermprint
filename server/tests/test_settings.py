class TestSettingsEndpoint:
    def test_get_settings_returns_defaults(self, client):
        resp = client.get("/api/settings")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ble_device_name"] == "X5h-10B5"
        assert data["width"] == 384
        assert data["quality"] == 50
        assert data["speed"] == 16
        assert data["energy"] == 0
        assert data["contrast"] == 1.0
        assert data["gamma"] == 1.0
        assert data["rotate"] == 0
        assert data["chunk_rows"] == 10
        assert data["chunk_delay"] == 0.2
        assert data["feed"] == 200

    def test_put_settings_updates_values(self, client):
        resp = client.put(
            "/api/settings",
            json={
                "ble_device_name": "MyPrinter",
                "width": 500,
                "quality": 53,
                "speed": 8,
                "energy": 500,
                "contrast": 1.5,
                "gamma": 0.9,
                "rotate": 90,
                "chunk_rows": 20,
                "chunk_delay": 0.5,
                "feed": 0,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ble_device_name"] == "MyPrinter"
        assert data["width"] == 500
        assert data["quality"] == 53
        assert data["speed"] == 8
        assert data["chunk_rows"] == 20

        get_resp = client.get("/api/settings")
        assert get_resp.json() == data

    def test_put_settings_partial_update(self, client):
        resp = client.put(
            "/api/settings",
            json={"width": 400},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["width"] == 400
        assert data["ble_device_name"] == "X5h-10B5"
