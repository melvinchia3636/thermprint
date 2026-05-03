class TestJobsEndpoint:
    def test_list_jobs_empty(self, client):
        resp = client.get("/api/jobs")
        assert resp.status_code == 200
        assert resp.json() == {"jobs": []}

    def test_get_job_not_found(self, client):
        resp = client.get("/api/jobs/nonexistent")
        assert resp.status_code == 404

    def test_get_job_after_create(self, client, test_image):
        create_resp = client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
        )
        job_id = create_resp.json()["job_id"]

        resp = client.get(f"/api/jobs/{job_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["job_id"] == job_id
        assert data["status"] == "queued"
        assert data["progress"] is None
        assert data["error"] is None
        assert data["created_at"] is not None

    def test_list_jobs_returns_created_jobs(self, client, test_image):
        client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
        )
        client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
        )
        resp = client.get("/api/jobs")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["jobs"]) == 2

    def test_cancel_job(self, client, test_image):
        create_resp = client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
        )
        job_id = create_resp.json()["job_id"]

        resp = client.delete(f"/api/jobs/{job_id}")
        assert resp.status_code == 204

        get_resp = client.get(f"/api/jobs/{job_id}")
        assert get_resp.json()["status"] == "done"
        assert get_resp.json()["progress"] == "cancelled"

    def test_cancel_nonexistent_job(self, client):
        resp = client.delete("/api/jobs/nonexistent")
        assert resp.status_code == 404
