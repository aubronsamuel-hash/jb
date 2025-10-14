from __future__ import annotations

from pathlib import Path

import pytest

from backend.app.data.sample_timesheets import load_sample_timesheet
from backend.app.services.payroll import (
    build_payroll_report,
    compute_payroll_report,
    payroll_report_to_csv,
    payroll_report_to_pdf,
    write_payroll_report,
)
from scripts import export_payroll_reports


def _assert_ascii(content: bytes | str) -> None:
    if isinstance(content, str):
        content.encode("ascii")
    else:
        content.decode("ascii")


def test_compute_payroll_report_totals() -> None:
    timesheet = load_sample_timesheet()
    report = compute_payroll_report(timesheet)
    assert report.period_start == "2024-06-10"
    assert report.period_end == "2024-06-16"
    assert report.total_hours == pytest.approx(32.5)
    assert report.total_gross_cents == 90700
    assert report.total_contributions_cents == 19954
    assert report.total_net_cents == 70746
    lines = {line.user_id: line for line in report.lines}
    assert lines["crew-sonia"].gross_cents == 28000
    assert lines["crew-sonia"].net_cents == 21840
    assert lines["crew-malik"].gross_cents == 31200
    assert lines["crew-malik"].net_cents == 24336
    assert lines["crew-ines"].gross_cents == 31500
    assert lines["crew-ines"].net_cents == 24570


def test_payroll_exports_are_ascii_and_deterministic(tmp_path: Path) -> None:
    report = build_payroll_report()
    csv_content = payroll_report_to_csv(report)
    pdf_bytes = payroll_report_to_pdf(report)
    _assert_ascii(csv_content)
    _assert_ascii(pdf_bytes)
    assert "crew-sonia" in csv_content
    assert csv_content.splitlines()[-1].startswith("TOTAL")
    assert pdf_bytes.startswith(b"%PDF-Stub 1.0")
    csv_path, pdf_path = write_payroll_report(report, tmp_path)
    assert csv_path.exists()
    assert pdf_path.exists()
    assert csv_path.read_text(encoding="utf-8") == csv_content
    assert pdf_path.read_bytes() == pdf_bytes


def test_export_script_cli_invocation(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = export_payroll_reports.main(["--out", str(tmp_path)])
    assert exit_code == 0
    captured = capsys.readouterr()
    csv_path = tmp_path / "payroll-report.csv"
    pdf_path = tmp_path / "payroll-report.pdf"
    assert csv_path.exists()
    assert pdf_path.exists()
    assert f"CSV: {csv_path}" in captured.out
    assert f"PDF: {pdf_path}" in captured.out
    report = build_payroll_report()
    assert csv_path.read_text(encoding="utf-8") == payroll_report_to_csv(report)
    assert pdf_path.read_bytes() == payroll_report_to_pdf(report)
