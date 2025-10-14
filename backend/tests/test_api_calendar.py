from backend.app.api.main import create_app
from backend.app.api.testing import ApiTestClient
from backend.app.data.sample_calendar_tokens import load_calendar_tokens


client = ApiTestClient(create_app())
TOKENS = load_calendar_tokens()


def test_calendar_assignments_returns_plain_text_feed() -> None:
    token = TOKENS["USER:crew-malik"]
    response = client.get(f"/api/calendar/assignments.ics?scope=USER:crew-malik&token={token}")
    assert response.status_code == 200
    assert response.content_type == "text/calendar; charset=utf-8"
    assert "BEGIN:VCALENDAR" in response.text
    response.text.encode("ascii")


def test_calendar_assignments_requires_token() -> None:
    response = client.get("/api/calendar/assignments.ics?scope=USER:crew-malik")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "missing_token"


def test_calendar_assignments_validates_token() -> None:
    token = TOKENS["USER:crew-malik"]
    response = client.get(f"/api/calendar/assignments.ics?scope=USER:crew-malik&token={token}-bad")
    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "invalid_token"


def test_calendar_assignments_validates_scope() -> None:
    token = TOKENS["ALL"]
    response = client.get(f"/api/calendar/assignments.ics?scope=INVALID&token={token}")
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "invalid_scope"
