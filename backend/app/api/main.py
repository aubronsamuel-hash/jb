from __future__ import annotations

from .app import HttpError, MicroApi, PlainTextResponse, Request
from ..config import API_TITLE, API_VERSION
from ..services.dashboard import build_dashboard_snapshot, serialize_snapshot, summarize_snapshot
from ..services.planning import (
    AssignmentCursorNotFound,
    AssignmentPaginationError,
    get_assignment_feed,
)
from ..services.operations import collect_operational_overview
from ..services.calendar import (
    InvalidScopeError,
    InvalidTokenError,
    build_calendar_feed,
)


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

    @app.get("/api/calendar/assignments.ics")
    def calendar_assignments(request: Request) -> PlainTextResponse:
        scope = request.query_params.get("scope")
        token = request.query_params.get("token")
        if token is None or not token.strip():
            raise HttpError.unprocessable("missing_token", "token query parameter is required")

        try:
            feed = build_calendar_feed(scope, token)
        except InvalidScopeError as error:
            raise HttpError.unprocessable("invalid_scope", str(error)) from error
        except InvalidTokenError as error:
            raise HttpError.unauthorized("invalid_token", str(error)) from error

        return PlainTextResponse(content=feed, content_type="text/calendar; charset=utf-8")

    return app


app = create_app()
