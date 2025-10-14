"""Budget variance ASCII helpers (Step 17)."""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Dict

from ..data.sample_snapshot import load_sample_snapshot
from ..models.orga import BudgetLine, DashboardSnapshot, Project

DEFAULT_ALERT_THRESHOLD = 2000


class BudgetThresholdError(ValueError):
    """Raised when the requested alert threshold is invalid."""


class BudgetReportNotFoundError(LookupError):
    """Raised when no budget lines are available."""


def _normalize_threshold(threshold: int | None) -> int:
    if threshold is None:
        return DEFAULT_ALERT_THRESHOLD
    if threshold < 0:
        raise BudgetThresholdError("threshold must be greater or equal to zero")
    return threshold


def _project_lookup(projects: Sequence[Project]) -> Dict[str, Project]:
    return {project.id: project for project in projects}


def _serialize_line(
    line: BudgetLine,
    project: Project | None,
    *,
    threshold: int,
) -> Dict[str, object]:
    planned = int(line.planned_amount)
    actual = int(line.actual_amount)
    delta = actual - planned
    percent = 0.0
    if planned:
        percent = round((delta / planned) * 100, 2)
    status = "ok"
    if abs(delta) >= threshold:
        status = "alert"
    return {
        "projectId": line.project_id,
        "projectName": project.name if project else "",
        "planned": planned,
        "actual": actual,
        "delta": delta,
        "deltaPercent": percent,
        "status": status,
    }


def collect_budget_variance(alert_threshold: int | None = None) -> Dict[str, object]:
    """Return the structured budget variance report."""

    threshold = _normalize_threshold(alert_threshold)
    snapshot: DashboardSnapshot = load_sample_snapshot()
    if not snapshot.budgets:
        raise BudgetReportNotFoundError("no budget lines available")

    projects = _project_lookup(snapshot.projects)
    rows = []
    total_planned = 0
    total_actual = 0
    alerts = 0

    for line in snapshot.budgets:
        project = projects.get(line.project_id)
        item = _serialize_line(line, project, threshold=threshold)
        rows.append(item)
        total_planned += int(line.planned_amount)
        total_actual += int(line.actual_amount)
        if item["status"] == "alert":
            alerts += 1

    rows.sort(key=lambda entry: abs(int(entry["delta"])), reverse=True)
    total_delta = total_actual - total_planned

    return {
        "generatedAt": snapshot.generated_at,
        "threshold": threshold,
        "projects": rows,
        "summary": {
            "totalProjects": len(rows),
            "alerts": alerts,
            "totalPlanned": total_planned,
            "totalActual": total_actual,
            "totalDelta": total_delta,
        },
    }


def render_budget_variance_ascii(payload: Mapping[str, object]) -> str:
    """Render the budget variance payload as an ASCII text block (CRLF)."""

    generated_at = str(payload.get("generatedAt", ""))
    threshold = payload.get("threshold")
    raw_projects = payload.get("projects", [])
    summary = payload.get("summary", {})

    lines: list[str] = []
    lines.append("BUDGET VARIANCE REPORT")
    lines.append("=" * 64)
    lines.append(f"Generated at: {generated_at}")
    if isinstance(threshold, int):
        lines.append(f"Alert threshold: +/-{threshold} EUR")
    else:
        lines.append("Alert threshold: n/a")
    lines.append("")

    project_items: Iterable[object] = []
    if isinstance(raw_projects, Iterable):
        project_items = raw_projects

    for item in project_items:
        if not isinstance(item, Mapping):
            continue
        project_id = str(item.get("projectId", ""))
        project_name = str(item.get("projectName", ""))
        planned = int(item.get("planned", 0))
        actual = int(item.get("actual", 0))
        delta = int(item.get("delta", 0))
        percent = float(item.get("deltaPercent", 0.0))
        status = str(item.get("status", ""))
        heading = project_name or project_id
        if project_name and project_id:
            heading = f"{project_name} ({project_id})"
        lines.append(heading)
        lines.append("-" * len(heading))
        sign = "+" if delta >= 0 else "-"
        lines.append(
            f"Planned: {planned} EUR | Actual: {actual} EUR | Delta: {sign}{abs(delta)} EUR"
        )
        lines.append(f"Delta %: {percent:+.2f}% | Status: {status.upper()}")
        lines.append("")

    total_projects = 0
    alerts_count = 0
    total_planned = 0
    total_actual = 0
    total_delta = 0
    if isinstance(summary, Mapping):
        total_projects = int(summary.get("totalProjects", 0))
        alerts_count = int(summary.get("alerts", 0))
        total_planned = int(summary.get("totalPlanned", 0))
        total_actual = int(summary.get("totalActual", 0))
        total_delta = int(summary.get("totalDelta", 0))

    lines.append("SUMMARY")
    lines.append("-" * 32)
    lines.append(f"Projects: {total_projects}")
    lines.append(f"Alerts: {alerts_count}")
    lines.append(f"Total planned: {total_planned} EUR")
    lines.append(f"Total actual: {total_actual} EUR")
    sign = "+" if total_delta >= 0 else "-"
    lines.append(f"Total delta: {sign}{abs(total_delta)} EUR")

    text = "\r\n".join(lines)
    return f"{text}\r\n"


__all__ = [
    "DEFAULT_ALERT_THRESHOLD",
    "BudgetReportNotFoundError",
    "BudgetThresholdError",
    "collect_budget_variance",
    "render_budget_variance_ascii",
]
