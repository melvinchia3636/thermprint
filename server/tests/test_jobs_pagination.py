class TestJobsPagination:
    def test_list_jobs_with_pagination(self, client, test_image):
        for _ in range(15):
            client.post(
                "/api/print",
                files={"image": ("test.png", test_image, "image/png")},
            )

        page1 = client.get("/api/jobs?offset=0&limit=10")
        assert page1.status_code == 200
        assert len(page1.json()["jobs"]) == 10
        assert page1.json()["total"] == 15

        page2 = client.get("/api/jobs?offset=10&limit=10")
        assert page2.status_code == 200
        assert len(page2.json()["jobs"]) == 5
        assert page2.json()["total"] == 15

    def test_list_jobs_default_limit(self, client, test_image):
        for _ in range(5):
            client.post(
                "/api/print",
                files={"image": ("test.png", test_image, "image/png")},
            )
        resp = client.get("/api/jobs")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["jobs"]) == 5
        assert data["total"] == 5
