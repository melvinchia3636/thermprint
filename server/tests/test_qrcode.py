class TestQRCodeEndpoint:
    def test_qrcode_preview_success(self, client):
        resp = client.post(
            "/api/qrcode/preview",
            data={"url": "https://example.com"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["preview_url"].startswith("data:image/png;base64,")
        assert data["width"] > 0
        assert data["height"] > 0

    def test_qrcode_preview_with_style(self, client):
        resp = client.post(
            "/api/qrcode/preview",
            data={"url": "https://example.com", "style": "circle", "size": 200},
        )
        assert resp.status_code == 200

    def test_qrcode_print_creates_job(self, client):
        resp = client.post(
            "/api/qrcode",
            data={"url": "https://example.com"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["job_id"] != ""
        assert data["status"] == "queued"

    def test_qrcode_print_with_size_and_style(self, client):
        resp = client.post(
            "/api/qrcode",
            data={"url": "https://example.com", "size": 200, "style": "rounded"},
        )
        assert resp.status_code == 201

    def test_qrcode_print_with_embed_image(self, client, test_image):
        resp = client.post(
            "/api/qrcode",
            data={"url": "https://example.com"},
            files={"embed_image": ("logo.png", test_image, "image/png")},
        )
        assert resp.status_code == 201
