"""Crew roster CSV helpers (Step 16)."""

from __future__ import annotations

import csv
from dataclasses import asdict
from datetime import datetime
from io import StringIO
from typing import Dict, Iterable, List, Mapping, Sequence

from ..data.sample_assignments import load_sample_assignments
from ..models.planning import Assignment

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DEFAULT_STATUSES: Sequence[str] = ("confirmed", "in-progress")


class RosterDateError(ValueError):
    """Raised when the requested roster date is invalid."""


class RosterNotFoundError(LookupError):
    """Raised when no assignments are available for the requested roster."""


def _parse_date(value: str) -> str:
    try:
        parsed = datetime.strptime(value, DATE_FORMAT)
    except ValueError as error:
        raise RosterDateError("date must follow YYYY-MM-DD format") from error
    return parsed.date().isoformat()


def _normalize_statuses(statuses: Sequence[str] | None) -> Sequence[str]:
    if statuses is None:
        return DEFAULT_STATUSES
    normalized: List[str] = []
    for status in statuses:
        stripped = status.strip().lower()
        if stripped:
            normalized.append(stripped)
    if not normalized:
        return DEFAULT_STATUSES
    return tuple(dict.fromkeys(normalized))


def _time_window(assignment: Assignment) -> str:
    start = datetime.strptime(assignment.starts_at, TIME_FORMAT)
    end = datetime.strptime(assignment.ends_at, TIME_FORMAT)
    return f"{start:%H:%M}-{end:%H:%M}"


def _serialize_assignment(assignment: Assignment) -> Dict[str, object]:
    base = asdict(assignment)
    return {
        "assignmentId": base["id"],
        "missionId": base["mission_id"],
        "missionTitle": base["mission_title"],
        "userId": base["user_id"],
        "userName": base["user_name"],
        "role": base["role"],
        "status": base["status"],
        "startsAt": base["starts_at"],
        "endsAt": base["ends_at"],
        "location": base["location"],
        "timeWindow": _time_window(assignment),
        "updatedAt": base["updated_at"],
    }


def _status_counts(assignments: Iterable[Mapping[str, object]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in assignments:
        status = str(item["status"]).lower()
        counts[status] = counts.get(status, 0) + 1
    return counts


def collect_roster(date: str, *, include_statuses: Sequence[str] | None = None) -> Dict[str, object]:
    """Return a structured roster payload for the requested date."""

    normalized_date = _parse_date(date)
    allowed_statuses = set(_normalize_statuses(include_statuses))

    serialized: List[Dict[str, object]] = []
    for assignment in load_sample_assignments():
        assignment_date = assignment.starts_at.split("T", 1)[0]
        if assignment_date != normalized_date:
            continue
        if assignment.status.lower() not in allowed_statuses:
            continue
        serialized.append(_serialize_assignment(assignment))

    if not serialized:
        raise RosterNotFoundError(f"no assignments found for {normalized_date}")

    serialized.sort(key=lambda item: item["startsAt"])  # type: ignore[index]
    latest_update = max(item["updatedAt"] for item in serialized)

    return {
        "date": normalized_date,
        "rows": serialized,
        "summary": {
            "count": len(serialized),
            "byStatus": _status_counts(serialized),
        },
        "generatedAt": latest_update,
    }


def render_roster_csv(payload: Mapping[str, object]) -> str:
    """Render the structured roster payload as CSV text with CRLF line endings."""

    date = str(payload.get("date", ""))
    rows = payload.get("rows", [])

    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")
    writer.writerow(
        [
            "date",
            "assignment_id",
            "mission_id",
            "mission_title",
            "user_id",
            "user_name",
            "role",
            "status",
            "starts_at",
            "ends_at",
            "time_window",
            "location",
            "updated_at",
        ]
    )

    if isinstance(rows, Iterable):
        for item in rows:
            if not isinstance(item, Mapping):
                continue
            writer.writerow(
                [
                    date,
                    item.get("assignmentId", ""),
                    item.get("missionId", ""),
                    item.get("missionTitle", ""),
                    item.get("userId", ""),
                    item.get("userName", ""),
                    item.get("role", ""),
                    item.get("status", ""),
                    item.get("startsAt", ""),
                    item.get("endsAt", ""),
                    item.get("timeWindow", ""),
                    item.get("location", ""),
                    item.get("updatedAt", ""),
                ]
            )

    return buffer.getvalue()


__all__ = [
    "collect_roster",
    "render_roster_csv",
    "RosterDateError",
    "RosterNotFoundError",
    "DEFAULT_STATUSES",
]
