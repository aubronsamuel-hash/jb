from __future__ import annotations

import pytest

from backend.app.services.operations import collect_operational_overview


def test_collect_operational_overview_returns_release_status() -> None:
    overview = collect_operational_overview(limit=2)
    assert overview["release"]["status"] == "ok"
    assert overview["release"]["version"] == "0.2.0"
    assert overview["planning"]["pageInfo"]["limit"] == 2
    assert len(overview["planning"]["sample"]) <= 2
    for identifier in overview["planning"]["sample"]:
        identifier.encode("ascii")


def test_collect_operational_overview_rejects_invalid_limit() -> None:
    with pytest.raises(ValueError):
        collect_operational_overview(limit=0)
