"""Deterministic sample data for the Orga dashboard."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Tuple

from ..models.orga import BudgetLine, DashboardSnapshot, Mission, Person, Project, RoleLoad

ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def _timestamp() -> str:
    return datetime(2024, 5, 6, 8, 0, tzinfo=timezone.utc).strftime(ISO_FORMAT)


def _projects() -> Tuple[Project, ...]:
    return (
        Project(id="p-aurora", name="Festival Aurora", status="active", start="2024-06-10", end="2024-06-18"),
        Project(id="p-riverside", name="Riverside Sessions", status="planning", start="2024-07-02", end="2024-07-12"),
    )


def _missions() -> Tuple[Mission, ...]:
    return (
        Mission(
            id="m-light-tech",
            project_id="p-aurora",
            title="Balance lumiere",
            status="confirmed",
            scheduled="2024-06-10",
            duration_hours=6,
        ),
        Mission(
            id="m-soundcheck",
            project_id="p-aurora",
            title="Soundcheck groupe A",
            status="in-progress",
            scheduled="2024-06-11",
            duration_hours=4,
        ),
        Mission(
            id="m-video-calibration",
            project_id="p-riverside",
            title="Calibration cameras",
            status="pending",
            scheduled="2024-07-04",
            duration_hours=5,
        ),
        Mission(
            id="m-stage-management",
            project_id="p-riverside",
            title="Coordination plateau",
            status="planned",
            scheduled="2024-07-05",
            duration_hours=3,
        ),
    )


def _people() -> Tuple[Person, ...]:
    return (
        Person(id="crew-sonia", full_name="Sonia Lefevre", role="son", availability="on-duty"),
        Person(id="crew-malik", full_name="Malik Roche", role="lumiere", availability="on-duty"),
        Person(id="crew-ines", full_name="Ines Martel", role="video", availability="standby"),
        Person(id="crew-jules", full_name="Jules Pinto", role="plateau", availability="off"),
    )


def _role_loads() -> Tuple[RoleLoad, ...]:
    return (
        RoleLoad(role="son", allocated_hours=28, available_hours=40),
        RoleLoad(role="lumiere", allocated_hours=30, available_hours=38),
        RoleLoad(role="video", allocated_hours=18, available_hours=32),
        RoleLoad(role="plateau", allocated_hours=12, available_hours=30),
    )


def _budgets() -> Tuple[BudgetLine, ...]:
    return (
        BudgetLine(project_id="p-aurora", planned_amount=42000, actual_amount=44800),
        BudgetLine(project_id="p-riverside", planned_amount=31000, actual_amount=30200),
    )


def _alerts() -> Tuple[str, ...]:
    return (
        "Conflit planning: mission Soundcheck groupe A overlap avec repetition video",
        "Budget depasse: Festival Aurora +2800 EUR",
        "Disponibilite critique: role video sous 60%",
    )


def load_sample_snapshot() -> DashboardSnapshot:
    """Return a deterministic snapshot for offline usage."""

    return DashboardSnapshot(
        generated_at=_timestamp(),
        projects=_projects(),
        missions=_missions(),
        people=_people(),
        role_loads=_role_loads(),
        budgets=_budgets(),
        alerts=_alerts(),
    )
