from __future__ import annotations

from backend.app.api.main import create_app
from backend.app.api.testing import ApiTestClient

client = ApiTestClient(create_app())


def test_role_utilization_endpoint_returns_ascii() -> None:
    response = client.get("/api/roles/role-utilization.txt")

    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert "ROLE UTILIZATION REPORT" in response.text
    assert "Status: ALERT" in response.text
    assert response.text.endswith("\r\n")


def test_role_utilization_endpoint_accepts_target_override() -> None:
    response = client.get("/api/roles/role-utilization.txt?target=60")

    assert response.status_code == 200
    assert "Target utilization: 60.0%" in response.text
    assert "Alerts: 2" in response.text


def test_role_utilization_endpoint_validates_target() -> None:
    response = client.get("/api/roles/role-utilization.txt?target=abc")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "invalid_target"

    response = client.get("/api/roles/role-utilization.txt?target=0")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "invalid_target"

    response = client.get("/api/roles/role-utilization.txt?target=150")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "invalid_target"
