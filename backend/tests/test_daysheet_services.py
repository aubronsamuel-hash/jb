import pytest

from backend.app.services.daysheet import (
    DaySheetDateError,
    DaySheetNotFoundError,
    collect_day_sheet,
    render_day_sheet_ascii,
)


def test_collect_day_sheet_returns_confirmed_assignment() -> None:
    payload = collect_day_sheet("2024-06-10")
    assert payload["date"] == "2024-06-10"
    assert payload["summary"]["count"] == 1
    assignment = payload["assignments"][0]
    assert assignment["user"]["name"] == "Malik Roche"
    assert assignment["timeWindow"] == "08:00-14:00"


def test_collect_day_sheet_can_include_pending() -> None:
    payload = collect_day_sheet("2024-07-04", include_statuses=("pending", "planned"))
    assert payload["summary"]["count"] == 1
    assert payload["assignments"][0]["status"] == "pending"


@pytest.mark.parametrize("value", ["2024/06/10", "10-06-2024", "", "2024-13-01"])
def test_collect_day_sheet_validates_date(value: str) -> None:
    with pytest.raises(DaySheetDateError):
        collect_day_sheet(value)


def test_collect_day_sheet_requires_assignments() -> None:
    with pytest.raises(DaySheetNotFoundError):
        collect_day_sheet("2024-01-01")


def test_render_day_sheet_ascii_is_ascii() -> None:
    payload = collect_day_sheet("2024-06-10")
    text = render_day_sheet_ascii(payload)
    assert text.endswith("\r\n")
    text.encode("ascii")
    assert "DAY SHEET 2024-06-10" in text
