from __future__ import annotations

from pathlib import Path

from scripts.export_budget_variance import export_budget_variance


def test_export_budget_variance_creates_ascii_file(tmp_path: Path) -> None:
    destination = tmp_path / "budget-variance.txt"

    path, payload = export_budget_variance(destination, threshold=5000)

    assert path == destination
    assert payload["threshold"] == 5000

    content = destination.read_bytes()
    assert content.endswith(b"\r\n")
    content.decode("ascii")
