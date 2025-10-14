"""Calendar ICS feed generation for Step 14."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, Tuple

from ..data.sample_assignments import load_sample_assignments
from ..data.sample_calendar_tokens import load_calendar_tokens
from ..models.planning import Assignment

CONFIRMED_STATUS = "confirmed"
SUPPORTED_PREFIXES = {"USER", "PROJECT", "ALL"}
PRODID = "-//Coulisses Crew//Planning//EN"


class InvalidScopeError(ValueError):
    """Raised when the requested scope does not match the supported format."""


class InvalidTokenError(PermissionError):
    """Raised when the provided token does not match the expected value."""


def normalize_scope(scope: str | None) -> str:
    """Return a normalized representation of the requested scope."""

    if scope is None:
        return "ALL"
    trimmed = scope.strip()
    if not trimmed:
        return "ALL"
    if trimmed.upper() == "ALL":
        return "ALL"
    if ":" not in trimmed:
        raise InvalidScopeError("scope must follow '<prefix>:<value>' format")
    prefix, value = trimmed.split(":", 1)
    prefix = prefix.upper()
    if prefix not in SUPPORTED_PREFIXES:
        raise InvalidScopeError("scope prefix must be USER, PROJECT or ALL")
    if not value:
        raise InvalidScopeError("scope value cannot be empty")
    return f"{prefix}:{value}"


def _split_scope(scope: str) -> Tuple[str, str | None]:
    if scope == "ALL":
        return "ALL", None
    prefix, value = scope.split(":", 1)
    return prefix, value


def _filter_confirmed(assignments: Iterable[Assignment]) -> Tuple[Assignment, ...]:
    return tuple(item for item in assignments if item.status == CONFIRMED_STATUS)


def _assignments_for_scope(scope: str) -> Tuple[Assignment, ...]:
    all_assignments = load_sample_assignments()
    confirmed = _filter_confirmed(all_assignments)
    prefix, value = _split_scope(scope)
    if prefix == "ALL":
        return confirmed
    if prefix == "USER":
        return tuple(item for item in confirmed if item.user_id == value)
    if prefix == "PROJECT":
        return tuple(item for item in confirmed if item.mission_id == value)
    raise InvalidScopeError(f"scope '{scope}' is not supported")


def _escape(text: str) -> str:
    escaped = text.replace("\\", "\\\\")
    escaped = escaped.replace(",", "\\,")
    escaped = escaped.replace(";", "\\;")
    escaped = escaped.replace("\n", "\\n")
    return escaped


def _iso_to_ics(value: str) -> str:
    timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return timestamp.strftime("%Y%m%dT%H%M%SZ")


def _resolve_calendar_name(scope: str, assignments: Tuple[Assignment, ...]) -> str:
    prefix, value = _split_scope(scope)
    if prefix == "ALL":
        return "Coulisses Crew - Confirmed Assignments"
    if prefix == "USER":
        for item in assignments:
            return f"{item.user_name} - Assignments"
        return f"{value} - Assignments"
    if prefix == "PROJECT":
        for item in assignments:
            return f"{item.mission_title} - Project"
        return f"{value} - Project"
    return "Coulisses Crew"


def _calendar_description(assignments: Tuple[Assignment, ...]) -> str:
    if assignments:
        return "Confirmed assignments exported from Coulisses Crew."
    return "No confirmed assignments available for this scope."


def _build_event_lines(assignment: Assignment) -> Tuple[str, ...]:
    return (
        "BEGIN:VEVENT",
        f"UID:{assignment.id}@coulisses-crew",
        f"DTSTAMP:{_iso_to_ics(assignment.updated_at)}",
        f"DTSTART:{_iso_to_ics(assignment.starts_at)}",
        f"DTEND:{_iso_to_ics(assignment.ends_at)}",
        f"SUMMARY:{_escape(assignment.mission_title)}",
        f"LOCATION:{_escape(assignment.location)}",
        f"DESCRIPTION:{_escape(assignment.user_name)} ({assignment.role})",
        "STATUS:CONFIRMED",
        "END:VEVENT",
    )


def generate_ics(scope: str | None) -> str:
    """Generate an ICS payload for the requested scope without token validation."""

    normalized_scope = normalize_scope(scope)
    assignments = _assignments_for_scope(normalized_scope)
    calendar_name = _resolve_calendar_name(normalized_scope, assignments)
    description = _calendar_description(assignments)

    lines = [
        "BEGIN:VCALENDAR",
        f"PRODID:{PRODID}",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{_escape(calendar_name)}",
        f"X-WR-CALDESC:{_escape(description)}",
    ]

    for assignment in assignments:
        lines.extend(_build_event_lines(assignment))

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def build_calendar_feed(scope: str | None, token: str) -> str:
    """Validate the provided token and return the ICS calendar feed."""

    normalized_scope = normalize_scope(scope)
    tokens = load_calendar_tokens()
    expected_token = tokens.get(normalized_scope)
    if expected_token is None:
        raise InvalidScopeError(f"scope '{normalized_scope}' is not registered")
    if not token:
        raise InvalidTokenError("token is required")
    if token != expected_token:
        raise InvalidTokenError("token mismatch for scope")
    return generate_ics(normalized_scope)


def available_scopes() -> Dict[str, str]:
    """Expose the deterministic scope/token mapping (useful for CLI tooling)."""

    return load_calendar_tokens().copy()


__all__ = [
    "available_scopes",
    "build_calendar_feed",
    "generate_ics",
    "InvalidScopeError",
    "InvalidTokenError",
    "normalize_scope",
]
