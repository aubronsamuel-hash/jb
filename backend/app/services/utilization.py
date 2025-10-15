"""Role utilization reporting helpers for Step 18."""
from __future__ import annotations

from typing import Dict, Iterable, Mapping

from ..data.sample_snapshot import load_sample_snapshot
from ..models.orga import DashboardSnapshot, RoleLoad

DEFAULT_UTILIZATION_TARGET = 0.75


class UtilizationTargetError(ValueError):
    """Raised when the requested utilization target ratio is invalid."""


class UtilizationReportNotFoundError(LookupError):
    """Raised when no role load data is available."""


def _normalize_target(target: float | None) -> float:
    if target is None:
        return DEFAULT_UTILIZATION_TARGET
    if target <= 0 or target > 1:
        raise UtilizationTargetError("target ratio must be between 0 and 1")
    return target


def _serialize_role(load: RoleLoad, *, target: float) -> Dict[str, object]:
    available = int(load.available_hours)
    allocated = int(load.allocated_hours)
    utilization = 0.0
    if available > 0:
        utilization = round(allocated / available, 2)
    status = "ok"
    if utilization >= target and available > 0:
        status = "alert"
    return {
        "role": load.role,
        "allocatedHours": allocated,
        "availableHours": available,
        "utilization": utilization,
        "status": status,
    }


def _sort_roles(items: Iterable[Mapping[str, object]]) -> list[Dict[str, object]]:
    return sorted(
        (
            {
                "role": str(item.get("role", "")),
                "allocatedHours": int(item.get("allocatedHours", 0)),
                "availableHours": int(item.get("availableHours", 0)),
                "utilization": float(item.get("utilization", 0.0)),
                "status": str(item.get("status", "")),
            }
            for item in items
        ),
        key=lambda entry: entry["utilization"],
        reverse=True,
    )


def collect_role_utilization(*, target_ratio: float | None = None) -> Dict[str, object]:
    """Return the structured role utilization report."""

    target = _normalize_target(target_ratio)
    snapshot: DashboardSnapshot = load_sample_snapshot()
    if not snapshot.role_loads:
        raise UtilizationReportNotFoundError("no role load data available")

    rows = []
    total_allocated = 0
    total_available = 0
    alerts = 0

    for load in snapshot.role_loads:
        item = _serialize_role(load, target=target)
        rows.append(item)
        total_allocated += item["allocatedHours"]
        total_available += item["availableHours"]
        if item["status"] == "alert":
            alerts += 1

    sorted_rows = _sort_roles(rows)
    average_utilization = 0.0
    if total_available > 0:
        average_utilization = round(total_allocated / total_available, 2)

    return {
        "generatedAt": snapshot.generated_at,
        "target": target,
        "roles": sorted_rows,
        "summary": {
            "totalRoles": len(sorted_rows),
            "alerts": alerts,
            "totalAllocated": total_allocated,
            "totalAvailable": total_available,
            "averageUtilization": average_utilization,
        },
    }


def render_role_utilization_ascii(payload: Mapping[str, object]) -> str:
    """Render the role utilization payload as an ASCII text block (CRLF)."""

    generated_at = str(payload.get("generatedAt", ""))
    target = payload.get("target")
    raw_roles = payload.get("roles", [])
    summary = payload.get("summary", {})

    lines: list[str] = []
    lines.append("ROLE UTILIZATION REPORT")
    lines.append("=" * 64)
    lines.append(f"Generated at: {generated_at}")
    if isinstance(target, (int, float)):
        percent = round(float(target) * 100, 1)
        lines.append(f"Target utilization: {percent}%")
    else:
        lines.append("Target utilization: n/a")
    lines.append("")

    role_items: Iterable[object] = []
    if isinstance(raw_roles, Iterable):
        role_items = raw_roles

    for item in role_items:
        if not isinstance(item, Mapping):
            continue
        role_name = str(item.get("role", ""))
        allocated = int(item.get("allocatedHours", 0))
        available = int(item.get("availableHours", 0))
        utilization = float(item.get("utilization", 0.0))
        status = str(item.get("status", ""))
        percent = round(utilization * 100, 1)
        lines.append(role_name or "(unknown role)")
        lines.append("-" * max(len(role_name), 13))
        lines.append(f"Allocated: {allocated}h | Available: {available}h")
        lines.append(f"Utilization: {percent}% | Status: {status.upper()}")
        lines.append("")

    total_roles = 0
    alerts_count = 0
    total_allocated = 0
    total_available = 0
    average_utilization = 0.0
    if isinstance(summary, Mapping):
        total_roles = int(summary.get("totalRoles", 0))
        alerts_count = int(summary.get("alerts", 0))
        total_allocated = int(summary.get("totalAllocated", 0))
        total_available = int(summary.get("totalAvailable", 0))
        average_utilization = float(summary.get("averageUtilization", 0.0))

    lines.append("SUMMARY")
    lines.append("-" * 32)
    lines.append(f"Roles: {total_roles}")
    lines.append(f"Alerts: {alerts_count}")
    lines.append(f"Total allocated: {total_allocated}h")
    lines.append(f"Total available: {total_available}h")
    lines.append(f"Average utilization: {round(average_utilization * 100, 1)}%")

    text = "\r\n".join(lines)
    return f"{text}\r\n"


__all__ = [
    "DEFAULT_UTILIZATION_TARGET",
    "UtilizationReportNotFoundError",
    "UtilizationTargetError",
    "collect_role_utilization",
    "render_role_utilization_ascii",
]
