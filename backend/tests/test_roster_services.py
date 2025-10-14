from __future__ import annotations

import pytest

from backend.app.services.roster import (
    RosterDateError,
    RosterNotFoundError,
    collect_roster,
    render_roster_csv,
)


def test_collect_roster_returns_confirmed_assignment() -> None:
    payload = collect_roster("2024-06-10")

    assert payload["date"] == "2024-06-10"
    rows = payload["rows"]
    assert isinstance(rows, list)
    assert rows
    first = rows[0]
    assert first["assignmentId"] == "asg-aurora-light-1"
    assert first["userName"] == "Malik Roche"
    assert first["timeWindow"] == "08:00-14:00"
    assert first["updatedAt"] == "2024-05-06T07:35:00Z"


def test_collect_roster_supports_status_filter() -> None:
    payload = collect_roster("2024-06-10", include_statuses=("declined",))

    rows = payload["rows"]
    assert len(rows) == 1
    assert rows[0]["assignmentId"] == "asg-aurora-light-2"
    assert rows[0]["status"] == "declined"


def test_collect_roster_validates_date() -> None:
    with pytest.raises(RosterDateError):
        collect_roster("10-06-2024")


def test_collect_roster_raises_when_empty() -> None:
    with pytest.raises(RosterNotFoundError):
        collect_roster("2024-01-01")


def test_render_roster_csv_produces_crlf_ascii() -> None:
    payload = collect_roster("2024-06-10", include_statuses=("confirmed", "declined"))

    csv_text = render_roster_csv(payload)
    assert csv_text.endswith("\r\n")
    assert "asg-aurora-light-1" in csv_text
    assert "asg-aurora-light-2" in csv_text
    csv_text.encode("ascii")
