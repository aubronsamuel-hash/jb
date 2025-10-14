"""Command line helper to export payroll reports."""
from __future__ import annotations

import argparse
from pathlib import Path

from backend.app.services.payroll import build_payroll_report, write_payroll_report


def export(out_dir: Path) -> tuple[Path, Path]:
    """Export the payroll report into the target directory."""

    report = build_payroll_report()
    return write_payroll_report(report, out_dir)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate payroll exports (CSV + PDF stub).")
    parser.add_argument(
        "--out",
        default="build/payroll",
        help="Output directory for generated files.",
    )
    args = parser.parse_args(argv)
    out_dir = Path(args.out)
    csv_path, pdf_path = export(out_dir)
    print(f"CSV: {csv_path}")
    print(f"PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
