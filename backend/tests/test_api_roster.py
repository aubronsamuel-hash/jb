from backend.app.api.main import create_app
from backend.app.api.testing import ApiTestClient


client = ApiTestClient(create_app())


def test_roster_endpoint_returns_csv() -> None:
    response = client.get("/api/rosters/crew-roster.csv?date=2024-06-10")
    assert response.status_code == 200
    assert response.content_type == "text/csv; charset=utf-8"
    assert "asg-aurora-light-1" in response.text
    assert "Malik Roche" in response.text
    assert response.text.endswith("\r\n")


def test_roster_endpoint_supports_statuses_filter() -> None:
    response = client.get(
        "/api/rosters/crew-roster.csv?date=2024-06-10&statuses=declined"
    )
    assert response.status_code == 200
    assert "asg-aurora-light-2" in response.text
    assert "declined" in response.text


def test_roster_endpoint_requires_date() -> None:
    response = client.get("/api/rosters/crew-roster.csv")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "missing_date"


def test_roster_endpoint_validates_date_format() -> None:
    response = client.get("/api/rosters/crew-roster.csv?date=10-06-2024")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "invalid_date"


def test_roster_endpoint_returns_404_when_empty() -> None:
    response = client.get("/api/rosters/crew-roster.csv?date=2024-01-01")
    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "roster_not_found"
