from __future__ import annotations

from .app import MicroApi
from ..services.dashboard import build_dashboard_snapshot, serialize_snapshot, summarize_snapshot

API_TITLE = "Orga Dashboard API"
API_VERSION = "0.2.0"


def create_app() -> MicroApi:
    """Instantiate the micro API and register routes."""

    app = MicroApi(title=API_TITLE, version=API_VERSION)

    @app.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/dashboard/snapshot")
    def dashboard_snapshot() -> dict[str, object]:
        snapshot = build_dashboard_snapshot()
        return serialize_snapshot(snapshot)

    @app.get("/api/dashboard/summary")
    def dashboard_summary() -> dict[str, object]:
        snapshot = build_dashboard_snapshot()
        return summarize_snapshot(snapshot)

    return app


app = create_app()
