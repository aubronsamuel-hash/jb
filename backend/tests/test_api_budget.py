from __future__ import annotations

from backend.app.api.main import create_app
from backend.app.api.testing import ApiTestClient

client = ApiTestClient(create_app())


def test_budget_variance_endpoint_returns_ascii() -> None:
    response = client.get("/api/budgets/budget-variance.txt")

    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert "BUDGET VARIANCE REPORT" in response.text
    assert "Status: ALERT" in response.text
    assert response.text.endswith("\r\n")


def test_budget_variance_endpoint_accepts_threshold_override() -> None:
    response = client.get("/api/budgets/budget-variance.txt?threshold=5000")

    assert response.status_code == 200
    assert "+/-5000" in response.text
    assert "Status: OK" in response.text
    assert "Alerts: 0" in response.text


def test_budget_variance_endpoint_validates_threshold() -> None:
    response = client.get("/api/budgets/budget-variance.txt?threshold=abc")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "invalid_threshold"

    response = client.get("/api/budgets/budget-variance.txt?threshold=-5")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "invalid_threshold"
