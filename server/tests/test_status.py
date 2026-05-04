class TestStatusEndpoint:
    def test_get_status(self, client):
        resp = client.get("/api/status")
        assert resp.status_code == 200
        assert resp.json()["connection"] in ("offline", "connecting", "online")
