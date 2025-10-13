from __future__ import annotations

import json
import re
from pathlib import Path

from backend.app.services.dashboard import build_dashboard_snapshot, serialize_snapshot, summarize_snapshot

SCHEMA_PATH = Path("tools/schemas/dashboard-snapshot.schema.json")


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate(instance: object, schema: dict) -> None:
    schema_type = schema.get("type")
    if schema_type == "object":
        assert isinstance(instance, dict), f"Expected object, got {type(instance)}"
        required = schema.get("required", [])
        for key in required:
            assert key in instance, f"Missing required property: {key}"
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in properties:
                validate(value, properties[key])
            elif not additional:
                raise AssertionError(f"Unexpected property: {key}")
        return
    if schema_type == "array":
        assert isinstance(instance, list), f"Expected array, got {type(instance)}"
        item_schema = schema.get("items")
        if item_schema:
            for item in instance:
                validate(item, item_schema)
        return
    if schema_type == "string":
        assert isinstance(instance, str), f"Expected string, got {type(instance)}"
        pattern = schema.get("pattern")
        if pattern:
            assert re.match(pattern, instance), f"String does not match pattern: {pattern}"
        return
    if schema_type == "integer":
        assert isinstance(instance, int), f"Expected integer, got {type(instance)}"
        minimum = schema.get("minimum")
        if minimum is not None:
            assert instance >= minimum, f"Value {instance} below minimum {minimum}"
        return
    if schema_type == "number":
        assert isinstance(instance, (int, float)), f"Expected number, got {type(instance)}"
        return
    if schema_type is None:
        return
    raise AssertionError(f"Schema type {schema_type} not supported in stub validator")


def test_build_dashboard_snapshot_is_deterministic():
    snapshot = build_dashboard_snapshot()
    assert snapshot.generated_at == "2024-05-06T08:00:00Z"
    assert len(snapshot.projects) == 2
    assert {mission.status for mission in snapshot.missions} == {
        "confirmed",
        "in-progress",
        "pending",
        "planned",
    }


def test_summarize_snapshot_produces_expected_kpis():
    snapshot = build_dashboard_snapshot()
    summary = summarize_snapshot(snapshot)
    assert summary["missions"]["total"] == 4
    assert summary["missions"]["byStatus"] == {
        "confirmed": 1,
        "in-progress": 1,
        "pending": 1,
        "planned": 1,
    }
    assert summary["missions"]["confirmedRatio"] == 25.0
    assert summary["projects"]["active"] == 2
    assert summary["budgets"] == [
        {"projectId": "p-aurora", "planned": 42000, "actual": 44800, "delta": 2800},
        {"projectId": "p-riverside", "planned": 31000, "actual": 30200, "delta": -800},
    ]
    assert summary["alerts"][0].startswith("Conflit planning")


def test_serialize_snapshot_respects_schema(tmp_path: Path):
    snapshot = build_dashboard_snapshot()
    payload = serialize_snapshot(snapshot)
    schema = load_schema()
    validate(payload, schema)
    exported = tmp_path / "snapshot.json"
    exported.write_text(json.dumps(payload), encoding="utf-8")
    assert exported.read_text(encoding="utf-8").startswith("{\"generatedAt\"")
