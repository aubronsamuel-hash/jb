from __future__ import annotations

from backend.app.api.main import create_app
from backend.app.api.testing import ApiTestClient


client = ApiTestClient(create_app())


def _assert_ascii(payload: str) -> None:
    payload.encode("ascii")


def test_assignments_feed_returns_default_page() -> None:
    response = client.get("/api/planning/assignments")
    assert response.status_code == 200
    body = response.json()
    assert body["pageInfo"]["limit"] == 2
    assert body["summary"]["total"] == 5
    assert len(body["items"]) == 2
    assert body["items"][0]["status"] == "confirmed"
    _assert_ascii(response.text)


def test_assignments_feed_rejects_invalid_limit() -> None:
    response = client.get("/api/planning/assignments?limit=0")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_pagination"
    _assert_ascii(response.text)


def test_assignments_feed_returns_not_found_for_cursor() -> None:
    response = client.get("/api/planning/assignments?cursor=missing")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "cursor_not_found"
    _assert_ascii(response.text)
