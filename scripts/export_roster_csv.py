import argparse
from pathlib import Path
from typing import Sequence

from backend.app.services.roster import collect_roster, render_roster_csv


def export_roster_csv(
    date: str, destination: Path, statuses: Sequence[str] | None = None
) -> tuple[Path, dict[str, object]]:
    """Generate the crew roster CSV for the given date and write it to disk."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = collect_roster(date, include_statuses=statuses)
    csv_text = render_roster_csv(payload)
    destination.write_text(csv_text, encoding="utf-8", newline="")
    return destination, payload


def _parse_statuses(value: str | None) -> tuple[str, ...] | None:
    if not value:
        return None
    parts = [item.strip() for item in value.split(",") if item.strip()]
    if not parts:
        return None
    return tuple(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export Coulisses Crew roster as ASCII CSV."
    )
    parser.add_argument("--date", required=True, help="Target date in YYYY-MM-DD format.")
    parser.add_argument(
        "--statuses",
        help="Optional comma separated statuses to include (default confirmed,in-progress).",
    )
    parser.add_argument(
        "--out",
        default="build/rosters/crew-roster.csv",
        help="Destination file for the exported roster.",
    )
    args = parser.parse_args(argv)

    statuses = _parse_statuses(args.statuses)
    path, payload = export_roster_csv(args.date, Path(args.out), statuses=statuses)
    summary = payload.get("summary", {})
    count = 0
    if isinstance(summary, dict):
        count = int(summary.get("count", 0))
    print(f"Date: {payload['date']}")
    print(f"Assignments: {count}")
    print(f"Output: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
