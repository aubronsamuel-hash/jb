"""Planning models used for assignment feeds."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Assignment:
    """Immutable assignment representation for planning QA scenarios."""

    id: str
    mission_id: str
    mission_title: str
    user_id: str
    user_name: str
    role: str
    status: str
    starts_at: str
    ends_at: str
    updated_at: str
    location: str


__all__ = ["Assignment"]
