"""CLI to export the dashboard snapshot JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from backend.app.services.dashboard import build_dashboard_snapshot, serialize_snapshot


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export the Orga dashboard snapshot JSON.")
    parser.add_argument(
        "--out",
        dest="output",
        default="frontend/public/data/dashboard-snapshot.json",
        help="Target file for the JSON export (default: %(default)s)",
    )
    parser.add_argument(
        "--indent",
        dest="indent",
        type=int,
        default=2,
        help="Indent level for the JSON payload.",
    )
    return parser.parse_args()


def export_dashboard_snapshot(output: Path, indent: int = 2) -> Path:
    snapshot = build_dashboard_snapshot()
    payload = serialize_snapshot(snapshot)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=indent, ensure_ascii=True) + "\n", encoding="utf-8")
    return output


def main() -> None:
    args = _parse_args()
    path = export_dashboard_snapshot(Path(args.output), indent=args.indent)
    print(f"Snapshot exported to {path.as_posix()}")


if __name__ == "__main__":
    main()
