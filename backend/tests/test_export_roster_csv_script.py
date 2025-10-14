from __future__ import annotations

from pathlib import Path

from scripts.export_roster_csv import export_roster_csv


def test_export_roster_csv_creates_ascii_crlf_file(tmp_path: Path) -> None:
    destination = tmp_path / "crew-roster.csv"

    path, payload = export_roster_csv("2024-06-10", destination)

    assert path == destination
    assert payload["date"] == "2024-06-10"

    content = destination.read_bytes()
    assert content.endswith(b"\r\n")
    assert b"\r\r\n" not in content
    content.decode("ascii")
