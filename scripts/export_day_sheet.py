import argparse
from pathlib import Path
from typing import Sequence

from backend.app.services.daysheet import collect_day_sheet, render_day_sheet_ascii


def export_day_sheet(
    date: str, destination: Path, statuses: Sequence[str] | None = None
) -> tuple[Path, dict[str, object]]:
    """Generate the day sheet for the given date and write it to disk."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = collect_day_sheet(date, include_statuses=statuses)
    text = render_day_sheet_ascii(payload)
    destination.write_text(text, encoding="utf-8", newline="")
    return destination, payload


def _parse_statuses(value: str | None) -> tuple[str, ...] | None:
    if not value:
        return None
    parts = [item.strip() for item in value.split(",") if item.strip()]
    if not parts:
        return None
    return tuple(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export Coulisses Crew day sheets (ASCII text).")
    parser.add_argument("--date", required=True, help="Target date in YYYY-MM-DD format.")
    parser.add_argument(
        "--statuses",
        help="Optional comma separated statuses to include (default confirmed,in-progress).",
    )
    parser.add_argument(
        "--out",
        default="build/day-sheets/day-sheet.txt",
        help="Destination file for the exported day sheet.",
    )
    args = parser.parse_args(argv)

    statuses = _parse_statuses(args.statuses)
    path, payload = export_day_sheet(args.date, Path(args.out), statuses=statuses)
    summary = payload["summary"]
    print(f"Date: {payload['date']}")
    print(f"Assignments: {summary['count']}")
    print(f"Output: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
