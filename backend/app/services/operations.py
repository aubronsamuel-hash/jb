"""Operational helpers to monitor the release health for Step 13."""
from __future__ import annotations

from typing import Dict, Iterable, List

from ..config import API_VERSION
from .dashboard import build_dashboard_snapshot, summarize_snapshot
from .planning import get_assignment_feed

DEFAULT_SAMPLE_LIMIT = 3


def _truncate_alerts(alerts: Iterable[str], limit: int = 5) -> List[str]:
    truncated: List[str] = []
    for alert in alerts:
        truncated.append(str(alert))
        if len(truncated) >= limit:
            break
    return truncated


def _extract_assignment_ids(items: Iterable[Dict[str, object]]) -> List[str]:
    ids: List[str] = []
    for item in items:
        identifier = item.get("id")
        if isinstance(identifier, str):
            ids.append(identifier)
    return ids


def collect_operational_overview(*, limit: int = DEFAULT_SAMPLE_LIMIT) -> Dict[str, object]:
    """Compose a release status overview using existing services."""

    if limit <= 0:
        raise ValueError("limit must be greater than zero")

    snapshot = build_dashboard_snapshot()
    summary = summarize_snapshot(snapshot)
    planning_feed = get_assignment_feed(cursor=None, limit=limit)

    alerts = _truncate_alerts(summary.get("alerts", []))
    sample_ids = _extract_assignment_ids(planning_feed.get("items", []))

    return {
        "release": {
            "version": API_VERSION,
            "status": "ok",
            "generatedAt": summary.get("generatedAt", ""),
        },
        "dashboard": {
            "missions": summary.get("missions", {}),
            "projects": summary.get("projects", {}),
            "alerts": alerts,
        },
        "planning": {
            "pageInfo": planning_feed.get("pageInfo", {}),
            "summary": planning_feed.get("summary", {}),
            "sample": sample_ids,
        },
    }


__all__ = ["collect_operational_overview", "DEFAULT_SAMPLE_LIMIT"]
