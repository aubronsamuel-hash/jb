"""CLI helper to inspect the release status overview."""
from __future__ import annotations

import argparse
import json
from typing import Any

from backend.app.services.operations import collect_operational_overview


def render_ascii(overview: dict[str, Any]) -> None:
    release = overview.get("release", {})
    dashboard = overview.get("dashboard", {})
    planning = overview.get("planning", {})

    version = release.get("version", "unknown")
    status = release.get("status", "unknown")
    generated_at = release.get("generatedAt", "")

    missions = dashboard.get("missions", {})
    total_missions = missions.get("total", 0)
    confirmed_ratio = missions.get("confirmedRatio", 0)
    alerts = dashboard.get("alerts", []) or ["none"]

    sample = planning.get("sample", [])

    print(f"Release version: {version}")
    print(f"Status: {status}")
    if generated_at:
        print(f"Generated at: {generated_at}")
    print(f"Missions total: {total_missions} (confirmed {confirmed_ratio}%)")
    print("Alerts: " + ", ".join(str(alert) for alert in alerts))
    print("Sample assignments: " + ", ".join(str(identifier) for identifier in sample))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect release health overview.")
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Nombre d assignments a inclure dans l echantillon.",
    )
    parser.add_argument(
        "--format",
        choices=("ascii", "json"),
        default="ascii",
        help="Format de sortie (ascii ou json).",
    )
    args = parser.parse_args(argv)

    try:
        overview = collect_operational_overview(limit=args.limit)
    except ValueError as error:
        parser.error(str(error))

    if args.format == "json":
        print(json.dumps(overview, ensure_ascii=True, indent=2))
    else:
        render_ascii(overview)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
