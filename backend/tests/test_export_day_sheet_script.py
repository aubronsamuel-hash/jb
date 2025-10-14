from __future__ import annotations

from pathlib import Path

from scripts.export_day_sheet import export_day_sheet


def test_export_day_sheet_creates_ascii_crlf_file(tmp_path: Path) -> None:
    destination = tmp_path / "day-sheet.txt"

    path, payload = export_day_sheet("2024-06-10", destination)

    assert path == destination
    assert payload["date"] == "2024-06-10"

    content = destination.read_bytes()
    assert content.endswith(b"\r\n")
    assert b"\r\r\n" not in content
    content.decode("ascii")
