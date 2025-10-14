from __future__ import annotations

from backend.app.api.main import create_app
from backend.app.api.testing import ApiTestClient
from backend.app.services.dashboard import build_dashboard_snapshot, serialize_snapshot, summarize_snapshot


client = ApiTestClient(create_app())


def _assert_ascii(payload: str) -> None:
    payload.encode("ascii")


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    _assert_ascii(response.text)


def test_snapshot_endpoint_matches_service_output() -> None:
    response = client.get("/api/dashboard/snapshot")
    assert response.status_code == 200
    expected = serialize_snapshot(build_dashboard_snapshot())
    assert response.json() == expected
    _assert_ascii(response.text)


def test_summary_endpoint_matches_service_output() -> None:
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    expected = summarize_snapshot(build_dashboard_snapshot())
    assert response.json() == expected
    _assert_ascii(response.text)
