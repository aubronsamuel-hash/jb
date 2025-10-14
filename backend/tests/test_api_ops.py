from __future__ import annotations

from backend.app.api.main import create_app
from backend.app.api.testing import ApiTestClient


client = ApiTestClient(create_app())


def test_ops_status_endpoint_returns_overview() -> None:
    response = client.get("/api/ops/status")
    assert response.status_code == 200
    body = response.json()
    assert body["release"]["status"] == "ok"
    assert body["release"]["version"] == "0.2.0"
    assert "missions" in body["dashboard"]
    assert "sample" in body["planning"]
    response.text.encode("ascii")


def test_ops_status_endpoint_supports_limit_query() -> None:
    response = client.get("/api/ops/status?limit=1")
    assert response.status_code == 200
    body = response.json()
    assert body["planning"]["pageInfo"]["limit"] == 1
    assert len(body["planning"]["sample"]) <= 1
