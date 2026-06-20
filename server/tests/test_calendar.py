class TestCalendarEndpoint:
    """End-to-end tests for the calendar preview and print endpoints."""

    # ------------------------------------------------------------------ preview
    def test_calendar_preview_success(self, client):
        resp = client.post(
            "/api/calendar/preview",
            data={"year": 2026, "month": 6},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["preview_url"].startswith("data:image/png;base64,")
        assert data["width"] == 384
        assert data["height"] > 0

    def test_calendar_preview_different_months_vary_height(self, client):
        resp1 = client.post(
            "/api/calendar/preview",
            data={"year": 2026, "month": 2},
        )
        resp2 = client.post(
            "/api/calendar/preview",
            data={"year": 2026, "month": 3},
        )
        assert resp1.status_code == 200
        assert resp2.status_code == 200
        assert resp1.json()["width"] == 384
        assert resp2.json()["width"] == 384
        # March 2026 has 6 week-rows, February has 5 — heights must differ.
        assert resp1.json()["height"] != resp2.json()["height"]

    def test_calendar_preview_default_current_year(self, client):
        resp = client.post(
            "/api/calendar/preview",
            data={"year": 2026, "month": 1},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["width"] == 384
        assert data["height"] > 0

    # ------------------------------------------------------------------ print
    def test_calendar_print_creates_job(self, client):
        resp = client.post(
            "/api/calendar",
            data={"year": 2026, "month": 6},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["job_id"] != ""
        assert data["status"] == "queued"

    def test_calendar_print_different_month(self, client):
        resp = client.post(
            "/api/calendar",
            data={"year": 2026, "month": 12},
        )
        assert resp.status_code == 201
        assert resp.json()["status"] == "queued"

    # ----------------------------------------------------------- validation
    def test_calendar_preview_rejects_year_too_low(self, client):
        resp = client.post(
            "/api/calendar/preview",
            data={"year": 1999, "month": 6},
        )
        assert resp.status_code == 422

    def test_calendar_preview_rejects_year_too_high(self, client):
        resp = client.post(
            "/api/calendar/preview",
            data={"year": 2101, "month": 6},
        )
        assert resp.status_code == 422

    def test_calendar_preview_rejects_month_too_low(self, client):
        resp = client.post(
            "/api/calendar/preview",
            data={"year": 2026, "month": 0},
        )
        assert resp.status_code == 422

    def test_calendar_preview_rejects_month_too_high(self, client):
        resp = client.post(
            "/api/calendar/preview",
            data={"year": 2026, "month": 13},
        )
        assert resp.status_code == 422

    def test_calendar_print_rejects_missing_year(self, client):
        resp = client.post(
            "/api/calendar",
            data={"month": 6},
        )
        assert resp.status_code == 422

    def test_calendar_print_rejects_missing_month(self, client):
        resp = client.post(
            "/api/calendar",
            data={"year": 2026},
        )
        assert resp.status_code == 422
