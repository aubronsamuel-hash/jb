from __future__ import annotations

import pytest

from backend.app.data.sample_snapshot import load_sample_snapshot
from backend.app.services.budgets import (
    DEFAULT_ALERT_THRESHOLD,
    BudgetReportNotFoundError,
    BudgetThresholdError,
    collect_budget_variance,
    render_budget_variance_ascii,
)


def test_collect_budget_variance_highlights_alerts() -> None:
    payload = collect_budget_variance()

    projects = {item["projectId"]: item for item in payload["projects"]}
    aurora = projects["p-aurora"]
    riverside = projects["p-riverside"]

    assert aurora["delta"] == 2800
    assert aurora["status"] == "alert"
    assert riverside["status"] == "ok"
    summary = payload["summary"]
    assert summary["alerts"] == 1
    assert summary["totalDelta"] == 2000
    assert payload["threshold"] == DEFAULT_ALERT_THRESHOLD


def test_collect_budget_variance_allows_custom_threshold() -> None:
    payload = collect_budget_variance(alert_threshold=5000)

    projects = {item["projectId"]: item for item in payload["projects"]}
    assert projects["p-aurora"]["status"] == "ok"
    assert payload["threshold"] == 5000


def test_collect_budget_variance_validates_threshold() -> None:
    with pytest.raises(BudgetThresholdError):
        collect_budget_variance(alert_threshold=-1)


def test_render_budget_variance_ascii_outputs_crlf_ascii() -> None:
    payload = collect_budget_variance()

    text = render_budget_variance_ascii(payload)
    assert text.startswith("BUDGET VARIANCE REPORT")
    assert "ALERT" in text
    assert text.endswith("\r\n")
    text.encode("ascii")


def test_collect_budget_variance_without_budgets(monkeypatch: pytest.MonkeyPatch) -> None:
    def _empty_snapshot():  # type: ignore[return-type]
        snapshot = load_sample_snapshot()
        return snapshot.__class__(
            generated_at=snapshot.generated_at,
            projects=snapshot.projects,
            missions=snapshot.missions,
            people=snapshot.people,
            role_loads=snapshot.role_loads,
            budgets=(),
            alerts=snapshot.alerts,
        )

    import backend.app.services.budgets as budgets_service

    monkeypatch.setattr(budgets_service, "load_sample_snapshot", _empty_snapshot)

    with pytest.raises(BudgetReportNotFoundError):
        collect_budget_variance()


