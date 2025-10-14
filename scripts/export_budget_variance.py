from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from backend.app.services.budgets import (
    DEFAULT_ALERT_THRESHOLD,
    collect_budget_variance,
    render_budget_variance_ascii,
)


def export_budget_variance(
    destination: Path, *, threshold: int | None = None
) -> tuple[Path, dict[str, Any]]:
    """Generate the budget variance ASCII report and write it to disk."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = collect_budget_variance(alert_threshold=threshold)
    text = render_budget_variance_ascii(payload)
    destination.write_text(text, encoding="utf-8", newline="")
    return destination, payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export Coulisses Crew budget variance report as ASCII text."
    )
    parser.add_argument(
        "--out",
        default="build/budgets/budget-variance.txt",
        help="Destination file for the exported report.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        help=f"Optional alert threshold in EUR (default {DEFAULT_ALERT_THRESHOLD}).",
    )
    args = parser.parse_args(argv)

    path, payload = export_budget_variance(Path(args.out), threshold=args.threshold)
    summary = payload.get("summary", {})
    total_projects = 0
    alerts = 0
    if isinstance(summary, dict):
        total_projects = int(summary.get("totalProjects", 0))
        alerts = int(summary.get("alerts", 0))

    print(f"Generated at: {payload['generatedAt']}")
    print(f"Threshold: +/-{payload['threshold']} EUR")
    print(f"Projects: {total_projects}")
    print(f"Alerts: {alerts}")
    print(f"Output: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
