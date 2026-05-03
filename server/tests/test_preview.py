class TestPreviewEndpoint:
    def test_preview_success(self, client, test_image):
        resp = client.post(
            "/api/preview",
            files={"image": ("test.png", test_image, "image/png")},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["preview_url"].startswith("data:image/png;base64,")
        assert isinstance(data["width"], int)
        assert isinstance(data["height"], int)
        assert data["width"] > 0
        assert data["height"] > 0

    def test_preview_with_custom_settings(self, client, test_image):
        resp = client.post(
            "/api/preview",
            files={"image": ("test.png", test_image, "image/png")},
            data={
                "width": 384,
                "contrast": 1.5,
                "gamma": 1.2,
                "rotate": 90,
                "ble_device_name": "X5h-10B5",
                "quality": 50,
                "speed": 16,
                "energy": 0,
                "chunk_rows": 10,
                "chunk_delay": 0.2,
                "feed": 200,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["width"] == 384
        # rotated 100x80 -> 80x384
        assert data["height"] > 0

    def test_preview_rejects_non_image(self, client):
        resp = client.post(
            "/api/preview",
            files={"image": ("test.txt", b"not an image", "text/plain")},
        )
        assert resp.status_code == 422

    def test_preview_with_rotate_180(self, client, test_image):
        resp = client.post(
            "/api/preview",
            files={"image": ("test.png", test_image, "image/png")},
            data={
                "width": 384,
                "rotate": 180,
                "ble_device_name": "X5h-10B5",
                "quality": 50,
                "speed": 16,
                "energy": 0,
                "contrast": 1.0,
                "gamma": 1.0,
                "chunk_rows": 10,
                "chunk_delay": 0.2,
                "feed": 200,
            },
        )
        assert resp.status_code == 200
