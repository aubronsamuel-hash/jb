from __future__ import annotations

from pathlib import Path

from scripts.export_role_utilization import export_role_utilization


def test_export_role_utilization_creates_ascii_file(tmp_path: Path) -> None:
    destination = tmp_path / "role-utilization.txt"

    path, payload = export_role_utilization(destination, target_percent=75)

    assert path == destination
    assert payload["summary"]["totalRoles"] >= 1

    content = destination.read_bytes()
    assert content.endswith(b"\r\n")
    content.decode("ascii")
