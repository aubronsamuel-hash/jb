"""Payroll computation services for Coulisses Crew baseline."""
from __future__ import annotations

import csv
from decimal import Decimal, ROUND_HALF_UP
from io import StringIO
from pathlib import Path
from typing import Dict, Tuple

from ..data.sample_timesheets import load_sample_timesheet
from ..models.payroll import PayrollLine, PayrollReport, Timesheet

DEFAULT_CHARGE_RATE = Decimal("0.22")


def _decimal(value: float | int | str) -> Decimal:
    return Decimal(str(value))


def _round_cents(amount: Decimal) -> int:
    return int(amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _format_money(cents: int) -> str:
    euros = cents // 100
    remainder = abs(cents) % 100
    sign = "-" if cents < 0 else ""
    return f"{sign}{euros}.{remainder:02d}"


def compute_payroll_report(timesheet: Timesheet, charge_rate: float | Decimal = DEFAULT_CHARGE_RATE) -> PayrollReport:
    """Aggregate timesheet entries into a payroll report."""

    rate = charge_rate if isinstance(charge_rate, Decimal) else Decimal(str(charge_rate))
    summary: Dict[str, Dict[str, object]] = {}
    total_hours_dec = Decimal("0")
    total_gross_cents = 0
    total_contrib_cents = 0

    for entry in timesheet.entries:
        user_summary = summary.setdefault(
            entry.user_id,
            {
                "user_name": entry.user_name,
                "role": entry.role,
                "hourly_rate_cents": entry.hourly_rate_cents,
                "hours": Decimal("0"),
                "gross_cents": 0,
            },
        )
        if user_summary["hourly_rate_cents"] != entry.hourly_rate_cents:
            raise ValueError("Inconsistent hourly rate for user")
        hours = _decimal(entry.hours)
        gross_cents = _round_cents(hours * _decimal(entry.hourly_rate_cents))
        user_summary["hours"] = user_summary["hours"] + hours
        user_summary["gross_cents"] = int(user_summary["gross_cents"]) + gross_cents

    lines: list[PayrollLine] = []
    for user_id in sorted(summary.keys()):
        data = summary[user_id]
        hours_dec = data["hours"]
        gross_cents = int(data["gross_cents"])
        contributions_cents = _round_cents(Decimal(gross_cents) * rate)
        net_cents = gross_cents - contributions_cents
        total_hours_dec += hours_dec
        total_gross_cents += gross_cents
        total_contrib_cents += contributions_cents
        lines.append(
            PayrollLine(
                user_id=user_id,
                user_name=str(data["user_name"]),
                role=str(data["role"]),
                total_hours=float(hours_dec),
                hourly_rate_cents=int(data["hourly_rate_cents"]),
                gross_cents=gross_cents,
                contributions_cents=contributions_cents,
                net_cents=net_cents,
            )
        )

    total_net_cents = total_gross_cents - total_contrib_cents

    return PayrollReport(
        period_start=timesheet.period_start,
        period_end=timesheet.period_end,
        currency=timesheet.currency,
        charge_rate=float(rate),
        lines=tuple(lines),
        total_hours=float(total_hours_dec),
        total_gross_cents=total_gross_cents,
        total_contributions_cents=total_contrib_cents,
        total_net_cents=total_net_cents,
    )


def build_payroll_report() -> PayrollReport:
    """Build the payroll report from the sample timesheet."""

    return compute_payroll_report(load_sample_timesheet())


def payroll_report_to_csv(report: PayrollReport) -> str:
    """Serialize the payroll report into a CSV string."""

    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(
        [
            "user_id",
            "user_name",
            "role",
            "total_hours",
            "hourly_rate",
            "gross",
            "contributions",
            "net",
        ]
    )
    for line in report.lines:
        writer.writerow(
            [
                line.user_id,
                line.user_name,
                line.role,
                f"{line.total_hours:.2f}",
                _format_money(line.hourly_rate_cents),
                _format_money(line.gross_cents),
                _format_money(line.contributions_cents),
                _format_money(line.net_cents),
            ]
        )
    writer.writerow(
        [
            "TOTAL",
            "",
            "",
            f"{report.total_hours:.2f}",
            "",
            _format_money(report.total_gross_cents),
            _format_money(report.total_contributions_cents),
            _format_money(report.total_net_cents),
        ]
    )
    return buffer.getvalue()


def payroll_report_to_pdf(report: PayrollReport) -> bytes:
    """Render a deterministic ASCII PDF stub for the payroll report."""

    lines = [
        "%PDF-Stub 1.0",
        "Payroll Report - Coulisses Crew",
        f"Period: {report.period_start} - {report.period_end}",
        f"Charge Rate: {int(round(report.charge_rate * 100))}%",
        "",
    ]
    for line in report.lines:
        lines.append(
            " ".join(
                [
                    line.user_id,
                    line.user_name,
                    f"hours={line.total_hours:.2f}",
                    f"gross={_format_money(line.gross_cents)}",
                    f"net={_format_money(line.net_cents)}",
                ]
            )
        )
    lines.extend(
        [
            "",
            f"Total Hours: {report.total_hours:.2f}",
            f"Total Gross: {_format_money(report.total_gross_cents)}",
            f"Total Net: {_format_money(report.total_net_cents)}",
        ]
    )
    content = "\n".join(lines) + "\n"
    return content.encode("ascii")


def write_payroll_report(report: PayrollReport, output_dir: Path) -> Tuple[Path, Path]:
    """Write the payroll report CSV and PDF stub to the output directory."""

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "payroll-report.csv"
    pdf_path = output_dir / "payroll-report.pdf"
    csv_path.write_text(payroll_report_to_csv(report), encoding="utf-8")
    pdf_path.write_bytes(payroll_report_to_pdf(report))
    return csv_path, pdf_path


def export_payroll_report(output_dir: Path) -> Tuple[Path, Path]:
    """Convenience wrapper that builds and writes the payroll report."""

    report = build_payroll_report()
    return write_payroll_report(report, output_dir)


__all__ = [
    "DEFAULT_CHARGE_RATE",
    "build_payroll_report",
    "compute_payroll_report",
    "export_payroll_report",
    "payroll_report_to_csv",
    "payroll_report_to_pdf",
    "write_payroll_report",
]
