"""Planning services derived from QA feedback for Step 12."""
from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, Tuple

from ..data.sample_assignments import load_sample_assignments
from ..models.planning import Assignment

DEFAULT_LIMIT = 2
MAX_LIMIT = 50


class AssignmentPaginationError(ValueError):
    """Raised when the requested pagination parameters are invalid."""


class AssignmentCursorNotFound(LookupError):
    """Raised when the requested cursor does not exist."""


def _sorted_assignments() -> Tuple[Assignment, ...]:
    assignments = sorted(load_sample_assignments(), key=lambda item: item.updated_at, reverse=True)
    return tuple(assignments)


def _normalize_limit(limit: int) -> int:
    if limit <= 0:
        raise AssignmentPaginationError("limit must be greater than zero")
    if limit > MAX_LIMIT:
        raise AssignmentPaginationError("limit exceeds maximum of 50")
    return limit


def _find_start_index(assignments: Tuple[Assignment, ...], cursor: str | None) -> int:
    if not cursor:
        return 0
    for index, item in enumerate(assignments):
        if item.id == cursor:
            return index + 1
    raise AssignmentCursorNotFound(f"cursor '{cursor}' was not found")


def _serialize_assignment(assignment: Assignment) -> Dict[str, object]:
    base = asdict(assignment)
    user = {"id": base.pop("user_id"), "name": base.pop("user_name"), "role": base.pop("role")}
    mission = {"id": base.pop("mission_id"), "title": base.pop("mission_title")}
    return {**base, "user": user, "mission": mission}


def _status_counts(assignments: Iterable[Assignment]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in assignments:
        counts[item.status] = counts.get(item.status, 0) + 1
    return counts


def get_assignment_feed(*, cursor: str | None, limit: int | None = None) -> Dict[str, object]:
    """Return a cursor paginated feed of assignments for QA validation."""

    effective_limit = _normalize_limit(DEFAULT_LIMIT if limit is None else limit)
    assignments = _sorted_assignments()
    start_index = _find_start_index(assignments, cursor)
    page_items = assignments[start_index : start_index + effective_limit]

    next_cursor = None
    if start_index + effective_limit < len(assignments):
        next_cursor = assignments[start_index + effective_limit - 1].id

    previous_cursor = None
    if start_index > 0:
        previous_cursor = assignments[start_index - 1].id

    serialized_items = [_serialize_assignment(item) for item in page_items]

    return {
        "items": serialized_items,
        "pageInfo": {
            "limit": effective_limit,
            "nextCursor": next_cursor,
            "previousCursor": previous_cursor,
        },
        "summary": {
            "total": len(assignments),
            "byStatus": _status_counts(assignments),
        },
        "generatedAt": assignments[0].updated_at if assignments else None,
    }


__all__ = [
    "AssignmentCursorNotFound",
    "AssignmentPaginationError",
    "DEFAULT_LIMIT",
    "MAX_LIMIT",
    "get_assignment_feed",
]
