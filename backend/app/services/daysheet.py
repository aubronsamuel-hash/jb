"""Day sheet helpers for ASCII exports (Step 15)."""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Dict, Iterable, List, Mapping, Sequence

from ..data.sample_assignments import load_sample_assignments
from ..models.planning import Assignment

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DEFAULT_STATUSES: Sequence[str] = ("confirmed", "in-progress")


class DaySheetDateError(ValueError):
    """Raised when the requested day sheet date is invalid."""


class DaySheetNotFoundError(LookupError):
    """Raised when no assignments are available for the requested day."""


def _parse_date(value: str) -> str:
    try:
        parsed = datetime.strptime(value, DATE_FORMAT)
    except ValueError as error:
        raise DaySheetDateError("date must follow YYYY-MM-DD format") from error
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
        "id": base["id"],
        "mission": {"id": base["mission_id"], "title": base["mission_title"]},
        "user": {
            "id": base["user_id"],
            "name": base["user_name"],
            "role": base["role"],
        },
        "status": base["status"],
        "startsAt": base["starts_at"],
        "endsAt": base["ends_at"],
        "updatedAt": base["updated_at"],
        "location": base["location"],
        "timeWindow": _time_window(assignment),
    }


def _status_counts(assignments: Iterable[Mapping[str, object]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in assignments:
        status = str(item["status"]).lower()
        counts[status] = counts.get(status, 0) + 1
    return counts


def collect_day_sheet(date: str, *, include_statuses: Sequence[str] | None = None) -> Dict[str, object]:
    """Return a structured day sheet payload for the requested date."""

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
        raise DaySheetNotFoundError(f"no assignments found for {normalized_date}")

    serialized.sort(key=lambda item: item["startsAt"])  # type: ignore[index]
    latest_update = max(item["updatedAt"] for item in serialized)

    return {
        "date": normalized_date,
        "assignments": serialized,
        "summary": {
            "count": len(serialized),
            "byStatus": _status_counts(serialized),
        },
        "generatedAt": latest_update,
    }


def render_day_sheet_ascii(payload: Mapping[str, object]) -> str:
    """Render the structured day sheet as an ASCII text block with CRLF."""

    date = str(payload.get("date", ""))
    assignments = payload.get("assignments", [])
    summary = payload.get("summary", {})
    lines: List[str] = []

    lines.append(f"DAY SHEET {date}")
    lines.append("=" * 64)

    for item in assignments:
        if not isinstance(item, Mapping):
            continue
        mission = item.get("mission", {})
        user = item.get("user", {})
        line_time = str(item.get("timeWindow", ""))
        line_title = str(mission.get("title", ""))
        line_location = str(item.get("location", ""))
        line_status = str(item.get("status", "")).upper()
        lines.append(f"{line_time} | {line_title} | {line_location}")
        lines.append(
            f"Tech: {user.get('name', '')} ({user.get('role', '')}) "
            f"[{line_status}]"
        )
        lines.append(
            "IDs: "
            f"assignment={item.get('id', '')} "
            f"mission={mission.get('id', '')} "
            f"user={user.get('id', '')}"
        )
        lines.append("")

    total = 0
    if isinstance(summary, Mapping):
        total = int(summary.get("count", 0))
    lines.append(f"Total assignments: {total}")

    by_status: Mapping[str, int] = {}
    if isinstance(summary, Mapping):
        raw = summary.get("byStatus", {})
        if isinstance(raw, Mapping):
            by_status = raw
    for status, count in sorted(by_status.items()):
        lines.append(f" - {status}: {count}")

    lines.append("")
    text = "\r\n".join(lines)
    return f"{text}\r\n"


__all__ = [
    "collect_day_sheet",
    "render_day_sheet_ascii",
    "DaySheetDateError",
    "DaySheetNotFoundError",
    "DEFAULT_STATUSES",
]
