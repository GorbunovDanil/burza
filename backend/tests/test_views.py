from rest_framework.test import APIClient
import pytest

# Dummy HTTP client used to replace httpx.Client
class DummyClient:
    def __init__(self, **kwargs):
        pass

    def post(self, *args, **kwargs):
        class R:
            status_code = 200
            def json(self_): return {}
        return R()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        pass


@pytest.fixture
def client():
    return APIClient()


def test_rating_endpoint(monkeypatch, client):
    # Patch httpx.Client in api.views
    monkeypatch.setattr("api.views.httpx.Client",
                        lambda **k: DummyClient(), raising=False)

    payload = [{"name": "X", "date": 1, "rating": 9, "sale": 0}]
    resp = client.post("/api/rating/", payload, format="json")
    assert resp.status_code == 200
    assert resp.json()["accepted"] == 1


def test_start_endpoint(monkeypatch, client):
    # Stub run_pipeline so nothing heavy runs
    monkeypatch.setattr("api.views.run_pipeline", lambda: None)
    resp = client.post("/api/start/", {}, format="json")
    assert resp.status_code == 200 and resp.json() == {"ok": True}
