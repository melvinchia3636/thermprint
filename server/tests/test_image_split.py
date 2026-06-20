class TestImageSplit:
    """Tests for split-col/row image printing."""

    def test_preview_2x2_split_width_doubled(self, client, test_image):
        resp = client.post(
            "/api/preview",
            files={"image": ("test.png", test_image, "image/png")},
            data={"split_cols": 2, "split_rows": 2, "width": 384},
        )
        assert resp.status_code == 200
        data = resp.json()
        # Two columns of 384 → preview width = 768
        assert data["width"] == 768
        assert data["height"] > 0
        assert data["preview_url"].startswith("data:image/png;base64,")

    def test_preview_1x3_split_same_dimensions_1_col(self, client, test_image):
        """With split_cols=1 the preview dimensions match the unsplit version."""
        resp1 = client.post(
            "/api/preview",
            files={"image": ("test.png", test_image, "image/png")},
            data={"split_cols": 1, "split_rows": 1, "width": 384},
        )
        resp2 = client.post(
            "/api/preview",
            files={"image": ("test.png", test_image, "image/png")},
            data={"split_cols": 1, "split_rows": 3, "width": 384},
        )
        assert resp1.status_code == 200
        assert resp2.status_code == 200
        # Same width since only 1 column; heights are also the same
        assert resp2.json()["width"] == resp1.json()["width"]
        assert resp2.json()["height"] == resp1.json()["height"]
        # Preview URL still works
        assert resp2.json()["preview_url"].startswith("data:image/png;base64,")

    def test_preview_3x1_split_wider(self, client, test_image):
        resp = client.post(
            "/api/preview",
            files={"image": ("test.png", test_image, "image/png")},
            data={"split_cols": 3, "split_rows": 1, "width": 384},
        )
        assert resp.status_code == 200
        assert resp.json()["width"] == 1152

    def test_print_split_creates_job(self, client, test_image):
        resp = client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
            data={"split_cols": 2, "split_rows": 2, "width": 384},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["job_id"] != ""
        assert data["status"] == "queued"

    def test_print_split_rejects_col_zero(self, client, test_image):
        resp = client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
            data={"split_cols": 0, "width": 384},
        )
        assert resp.status_code == 422

    def test_preview_rejects_row_too_high(self, client, test_image):
        resp = client.post(
            "/api/preview",
            files={"image": ("test.png", test_image, "image/png")},
            data={"split_rows": 11, "width": 384},
        )
        assert resp.status_code == 422
