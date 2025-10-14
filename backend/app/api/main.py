from __future__ import annotations

from .app import HttpError, MicroApi, Request
from ..config import API_TITLE, API_VERSION
from ..services.dashboard import build_dashboard_snapshot, serialize_snapshot, summarize_snapshot
from ..services.planning import (
    AssignmentCursorNotFound,
    AssignmentPaginationError,
    get_assignment_feed,
)
from ..services.operations import collect_operational_overview


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

    @app.get("/api/planning/assignments")
    def planning_assignments(request: Request) -> dict[str, object]:
        limit_param = request.query_params.get("limit")
        cursor = request.query_params.get("cursor") or None

        limit_value: int | None = None
        if limit_param:
            try:
                limit_value = int(limit_param)
            except ValueError as error:
                raise HttpError.unprocessable("invalid_limit", "limit must be an integer") from error

        try:
            return get_assignment_feed(cursor=cursor, limit=limit_value)
        except AssignmentCursorNotFound as error:
            raise HttpError.not_found("cursor_not_found", str(error)) from error
        except AssignmentPaginationError as error:
            raise HttpError.unprocessable("invalid_pagination", str(error)) from error

    @app.get("/api/ops/status")
    def ops_status(request: Request) -> dict[str, object]:
        limit_param = request.query_params.get("limit")
        limit_value: int | None = None
        if limit_param:
            try:
                limit_value = int(limit_param)
            except ValueError as error:
                raise HttpError.unprocessable("invalid_limit", "limit must be an integer") from error

        try:
            if limit_value is None:
                return collect_operational_overview()
            return collect_operational_overview(limit=limit_value)
        except ValueError as error:
            raise HttpError.unprocessable("invalid_limit", str(error)) from error

    return app


app = create_app()
