"""Dataclasses representing timesheets and payroll reports."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class TimesheetEntry:
    """Single line of work declared by a crew member."""

    user_id: str
    user_name: str
    mission_id: str
    mission_title: str
    date: str
    role: str
    hours: float
    hourly_rate_cents: int


@dataclass(frozen=True)
class Timesheet:
    """Collection of timesheet entries covering a period."""

    period_start: str
    period_end: str
    currency: str
    entries: Tuple[TimesheetEntry, ...]


@dataclass(frozen=True)
class PayrollLine:
    """Aggregated payroll data for one crew member."""

    user_id: str
    user_name: str
    role: str
    total_hours: float
    hourly_rate_cents: int
    gross_cents: int
    contributions_cents: int
    net_cents: int


@dataclass(frozen=True)
class PayrollReport:
    """Summary payroll report for a timesheet period."""

    period_start: str
    period_end: str
    currency: str
    charge_rate: float
    lines: Tuple[PayrollLine, ...]
    total_hours: float
    total_gross_cents: int
    total_contributions_cents: int
    total_net_cents: int


__all__ = [
    "TimesheetEntry",
    "Timesheet",
    "PayrollLine",
    "PayrollReport",
]
