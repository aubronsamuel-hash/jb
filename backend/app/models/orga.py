"""Domain models for the Orga dashboard snapshot."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Project:
    """A project produced by the organisation."""

    id: str
    name: str
    status: str
    start: str
    end: str


@dataclass(frozen=True)
class Mission:
    """A mission planned within a project."""

    id: str
    project_id: str
    title: str
    status: str
    scheduled: str
    duration_hours: int


@dataclass(frozen=True)
class Person:
    """A crew member with a primary role."""

    id: str
    full_name: str
    role: str
    availability: str


@dataclass(frozen=True)
class RoleLoad:
    """Workload allocation for a specific role."""

    role: str
    allocated_hours: int
    available_hours: int


@dataclass(frozen=True)
class BudgetLine:
    """Budget tracking for a project."""

    project_id: str
    planned_amount: int
    actual_amount: int


@dataclass(frozen=True)
class DashboardSnapshot:
    """Immutable snapshot consumed by the dashboard."""

    generated_at: str
    projects: Tuple[Project, ...]
    missions: Tuple[Mission, ...]
    people: Tuple[Person, ...]
    role_loads: Tuple[RoleLoad, ...]
    budgets: Tuple[BudgetLine, ...]
    alerts: Tuple[str, ...]
