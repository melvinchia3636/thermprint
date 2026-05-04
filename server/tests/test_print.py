class TestPrintEndpoint:
    def test_print_creates_job(self, client, test_image):
        resp = client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["job_id"] != ""
        assert data["status"] == "queued"

    def test_print_with_custom_settings(self, client, test_image):
        resp = client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
            data={
                "width": 384,
                "quality": 51,
                "speed": 20,
                "energy": 100,
                "contrast": 1.2,
                "gamma": 0.8,
                "rotate": 0,
                "chunk_rows": 15,
                "chunk_delay": 0.3,
                "feed": 300,
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["status"] == "queued"

    def test_print_rejects_non_image(self, client):
        resp = client.post(
            "/api/print",
            files={"image": ("test.txt", b"not an image", "text/plain")},
        )
        assert resp.status_code == 422
