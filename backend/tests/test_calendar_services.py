from __future__ import annotations

import pytest

from backend.app.data.sample_calendar_tokens import load_calendar_tokens
from backend.app.services.calendar import (
    InvalidScopeError,
    InvalidTokenError,
    available_scopes,
    build_calendar_feed,
    normalize_scope,
)


TOKENS = load_calendar_tokens()


def _assert_ascii(value: str) -> None:
    value.encode("ascii")


def test_build_calendar_feed_returns_ics_payload() -> None:
    token = TOKENS["USER:crew-malik"]
    payload = build_calendar_feed("USER:crew-malik", token)
    _assert_ascii(payload)
    assert "BEGIN:VCALENDAR" in payload
    assert "SUMMARY:Balance lumiere" in payload
    assert payload.endswith("\r\n")


def test_build_calendar_feed_validates_token() -> None:
    token = TOKENS["USER:crew-malik"]
    with pytest.raises(InvalidTokenError):
        build_calendar_feed("USER:crew-malik", token + "-wrong")


def test_generate_ics_for_empty_user_scope_contains_notice() -> None:
    token = TOKENS["USER:crew-ines"]
    payload = build_calendar_feed("USER:crew-ines", token)
    assert "No confirmed assignments" in payload
    assert "BEGIN:VEVENT" not in payload


@pytest.mark.parametrize(
    "raw, expected",
    [
        (None, "ALL"),
        ("", "ALL"),
        ("all", "ALL"),
        ("USER:crew-malik", "USER:crew-malik"),
    ],
)
def test_normalize_scope_handles_expected_inputs(raw: str | None, expected: str) -> None:
    assert normalize_scope(raw) == expected


def test_available_scopes_matches_tokens() -> None:
    assert available_scopes() == TOKENS


def test_normalize_scope_rejects_invalid_formats() -> None:
    with pytest.raises(InvalidScopeError):
        normalize_scope("invalid")
