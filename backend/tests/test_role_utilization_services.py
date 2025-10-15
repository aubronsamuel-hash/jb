from __future__ import annotations

from backend.app.services.utilization import (
    DEFAULT_UTILIZATION_TARGET,
    UtilizationTargetError,
    collect_role_utilization,
    render_role_utilization_ascii,
)


def test_collect_role_utilization_marks_alert_and_sorts() -> None:
    payload = collect_role_utilization()

    roles = payload["roles"]
    assert roles[0]["role"] == "lumiere"
    assert roles[0]["status"] == "alert"

    summary = payload["summary"]
    assert summary["alerts"] == 1
    assert summary["totalRoles"] == len(roles)


def test_collect_role_utilization_supports_custom_target() -> None:
    payload = collect_role_utilization(target_ratio=0.6)

    statuses = {item["role"]: item["status"] for item in payload["roles"]}
    assert statuses["son"] == "alert"
    assert statuses["lumiere"] == "alert"


def test_collect_role_utilization_validates_target_ratio() -> None:
    try:
        collect_role_utilization(target_ratio=0)
    except UtilizationTargetError:
        pass
    else:
        raise AssertionError("expected UtilizationTargetError")


def test_render_role_utilization_ascii_returns_crlf() -> None:
    payload = collect_role_utilization(target_ratio=DEFAULT_UTILIZATION_TARGET)

    text = render_role_utilization_ascii(payload)

    assert text.endswith("\r\n")
    assert "ROLE UTILIZATION REPORT" in text
    assert "Status: ALERT" in text
