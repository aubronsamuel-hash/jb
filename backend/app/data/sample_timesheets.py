"""Deterministic timesheet data used for payroll calculations."""
from __future__ import annotations

from typing import Tuple

from ..models.payroll import Timesheet, TimesheetEntry


def _entries() -> Tuple[TimesheetEntry, ...]:
    return (
        TimesheetEntry(
            user_id="crew-sonia",
            user_name="Sonia Lefevre",
            mission_id="m-light-tech",
            mission_title="Balance lumiere",
            date="2024-06-10",
            role="lumiere",
            hours=6.0,
            hourly_rate_cents=2800,
        ),
        TimesheetEntry(
            user_id="crew-sonia",
            user_name="Sonia Lefevre",
            mission_id="m-soundcheck",
            mission_title="Soundcheck groupe A",
            date="2024-06-11",
            role="lumiere",
            hours=4.0,
            hourly_rate_cents=2800,
        ),
        TimesheetEntry(
            user_id="crew-malik",
            user_name="Malik Roche",
            mission_id="m-soundcheck",
            mission_title="Soundcheck groupe A",
            date="2024-06-11",
            role="son",
            hours=5.0,
            hourly_rate_cents=2600,
        ),
        TimesheetEntry(
            user_id="crew-malik",
            user_name="Malik Roche",
            mission_id="m-stage-management",
            mission_title="Coordination plateau",
            date="2024-06-12",
            role="son",
            hours=7.0,
            hourly_rate_cents=2600,
        ),
        TimesheetEntry(
            user_id="crew-ines",
            user_name="Ines Martel",
            mission_id="m-video-calibration",
            mission_title="Calibration cameras",
            date="2024-06-12",
            role="video",
            hours=4.5,
            hourly_rate_cents=3000,
        ),
        TimesheetEntry(
            user_id="crew-ines",
            user_name="Ines Martel",
            mission_id="m-video-calibration",
            mission_title="Calibration cameras",
            date="2024-06-13",
            role="video",
            hours=6.0,
            hourly_rate_cents=3000,
        ),
    )


def load_sample_timesheet() -> Timesheet:
    """Return a deterministic timesheet covering a fixed week."""

    return Timesheet(
        period_start="2024-06-10",
        period_end="2024-06-16",
        currency="EUR",
        entries=_entries(),
    )


__all__ = ["load_sample_timesheet"]
