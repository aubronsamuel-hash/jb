from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from backend.app.services.utilization import (
    DEFAULT_UTILIZATION_TARGET,
    collect_role_utilization,
    render_role_utilization_ascii,
)


def export_role_utilization(
    destination: Path, *, target_percent: float | None = None
) -> tuple[Path, dict[str, Any]]:
    """Generate the role utilization ASCII report and write it to disk."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    target_ratio: float | None = None
    if target_percent is not None:
        target_ratio = target_percent / 100.0
    payload = collect_role_utilization(target_ratio=target_ratio)
    text = render_role_utilization_ascii(payload)
    destination.write_text(text, encoding="utf-8", newline="")
    return destination, payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export Coulisses Crew role utilization report as ASCII text."
    )
    parser.add_argument(
        "--out",
        default="build/roles/role-utilization.txt",
        help="Destination file for the exported report.",
    )
    parser.add_argument(
        "--target",
        type=float,
        help=(
            "Optional utilization target in percent"
            f" (default {int(DEFAULT_UTILIZATION_TARGET * 100)})."
        ),
    )
    args = parser.parse_args(argv)

    target_percent: float | None = None
    if args.target is not None:
        if args.target <= 0 or args.target > 100:
            parser.error("--target must be within 0 and 100")
        target_percent = float(args.target)

    path, payload = export_role_utilization(Path(args.out), target_percent=target_percent)

    summary = payload.get("summary", {})
    total_roles = 0
    alerts = 0
    if isinstance(summary, dict):
        total_roles = int(summary.get("totalRoles", 0))
        alerts = int(summary.get("alerts", 0))

    target_ratio = payload.get("target", DEFAULT_UTILIZATION_TARGET)
    target_display = round(float(target_ratio) * 100, 1)

    print(f"Generated at: {payload['generatedAt']}")
    print(f"Target utilization: {target_display}%")
    print(f"Roles: {total_roles}")
    print(f"Alerts: {alerts}")
    print(f"Output: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
