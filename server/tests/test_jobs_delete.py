class TestJobsDeleteEndpoint:
    def test_delete_completed_job(self, client, test_image):
        create_resp = client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
        )
        job_id = create_resp.json()["job_id"]

        cancel_resp = client.delete(f"/api/jobs/{job_id}")
        assert cancel_resp.status_code == 204

        resp = client.delete(f"/api/jobs/{job_id}/delete")
        assert resp.status_code == 204

        get_resp = client.get(f"/api/jobs/{job_id}")
        assert get_resp.status_code == 404

    def test_delete_nonexistent_job(self, client):
        resp = client.delete("/api/jobs/nonexistent/delete")
        assert resp.status_code == 404

    def test_delete_active_job_returns_404(self, client, test_image):
        create_resp = client.post(
            "/api/print",
            files={"image": ("test.png", test_image, "image/png")},
        )
        job_id = create_resp.json()["job_id"]

        resp = client.delete(f"/api/jobs/{job_id}/delete")
        assert resp.status_code == 404
