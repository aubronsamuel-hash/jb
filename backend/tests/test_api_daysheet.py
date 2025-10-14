from backend.app.api.testing import ApiTestClient

from backend.app.api.main import create_app


client = ApiTestClient(create_app())


def test_day_sheet_endpoint_returns_text() -> None:
    response = client.get("/api/daysheets/day-sheet.txt?date=2024-06-10")
    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert "Malik Roche" in response.text
    assert "DAY SHEET 2024-06-10" in response.text
    response.text.encode("ascii")


def test_day_sheet_endpoint_supports_statuses_filter() -> None:
    response = client.get(
        "/api/daysheets/day-sheet.txt?date=2024-07-04&statuses=pending, planned"
    )
    assert response.status_code == 200
    assert "Calibration cameras" in response.text
    assert "[PENDING]" in response.text


def test_day_sheet_endpoint_requires_date() -> None:
    response = client.get("/api/daysheets/day-sheet.txt")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "missing_date"


def test_day_sheet_endpoint_validates_date_format() -> None:
    response = client.get("/api/daysheets/day-sheet.txt?date=10-06-2024")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "invalid_date"


def test_day_sheet_endpoint_returns_404_when_empty() -> None:
    response = client.get("/api/daysheets/day-sheet.txt?date=2024-01-01")
    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "day_sheet_not_found"
