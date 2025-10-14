from __future__ import annotations

from pathlib import Path

from backend.app.data.sample_calendar_tokens import load_calendar_tokens
from scripts.export_calendar_feed import export


TOKENS = load_calendar_tokens()


def test_export_preserves_crlf(tmp_path: Path) -> None:
    destination = tmp_path / "calendar.ics"
    export("USER:crew-malik", TOKENS["USER:crew-malik"], destination)
    payload = destination.read_bytes()

    assert payload.endswith(b"\r\n")
    assert b"\r\r\n" not in payload
    payload.decode("ascii")
