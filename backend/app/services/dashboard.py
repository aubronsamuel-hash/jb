"""Dashboard snapshot services."""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Dict, Iterable, List

from ..data.sample_snapshot import load_sample_snapshot
from ..models.orga import DashboardSnapshot


def build_dashboard_snapshot() -> DashboardSnapshot:
    """Compose the dashboard snapshot from the sample data provider."""

    return load_sample_snapshot()


def summarize_snapshot(snapshot: DashboardSnapshot) -> Dict[str, object]:
    """Compute KPIs for the dashboard view."""

    status_counts: Dict[str, int] = {}
    for mission in snapshot.missions:
        status_counts[mission.status] = status_counts.get(mission.status, 0) + 1

    role_load_summary: List[Dict[str, object]] = []
    for load in snapshot.role_loads:
        utilization = 0.0
        if load.available_hours:
            utilization = load.allocated_hours / load.available_hours
        role_load_summary.append(
            {
                "role": load.role,
                "allocatedHours": load.allocated_hours,
                "availableHours": load.available_hours,
                "utilization": round(utilization, 2),
            }
        )

    budget_summary: List[Dict[str, object]] = []
    for line in snapshot.budgets:
        delta = line.actual_amount - line.planned_amount
        budget_summary.append(
            {
                "projectId": line.project_id,
                "planned": line.planned_amount,
                "actual": line.actual_amount,
                "delta": delta,
            }
        )

    alerts = list(snapshot.alerts)

    active_projects = [project for project in snapshot.projects if project.status != "archived"]
    confirmed = status_counts.get("confirmed", 0)
    missions_total = len(snapshot.missions)
    confirmed_ratio = round((confirmed / missions_total) * 100, 1) if missions_total else 0.0

    return {
        "generatedAt": snapshot.generated_at,
        "missions": {"total": missions_total, "byStatus": status_counts, "confirmedRatio": confirmed_ratio},
        "projects": {"active": len(active_projects)},
        "roles": role_load_summary,
        "budgets": budget_summary,
        "alerts": alerts,
    }


def _serialize_collection(items: Iterable[object]) -> List[Dict[str, object]]:
    serialized: List[Dict[str, object]] = []
    for item in items:
        if is_dataclass(item):
            serialized.append(asdict(item))
        elif isinstance(item, dict):
            serialized.append(item)
        else:
            raise TypeError(f"Unsupported item for serialization: {item!r}")
    return serialized


def serialize_snapshot(snapshot: DashboardSnapshot) -> Dict[str, object]:
    """Serialize the snapshot to plain Python dictionaries and lists."""

    return {
        "generatedAt": snapshot.generated_at,
        "projects": _serialize_collection(snapshot.projects),
        "missions": _serialize_collection(snapshot.missions),
        "people": _serialize_collection(snapshot.people),
        "roleLoads": _serialize_collection(snapshot.role_loads),
        "budgets": _serialize_collection(snapshot.budgets),
        "alerts": list(snapshot.alerts),
    }
