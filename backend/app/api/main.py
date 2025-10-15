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
from ..services.budgets import (
    BudgetReportNotFoundError,
    BudgetThresholdError,
    collect_budget_variance,
    render_budget_variance_ascii,
)
from ..services.daysheet import (
    DaySheetDateError,
    DaySheetNotFoundError,
    collect_day_sheet,
    render_day_sheet_ascii,
)
from ..services.roster import (
    RosterDateError,
    RosterNotFoundError,
    collect_roster,
    render_roster_csv,
)
from ..services.utilization import (
    UtilizationReportNotFoundError,
    UtilizationTargetError,
    collect_role_utilization,
    render_role_utilization_ascii,
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

    @app.get("/api/daysheets/day-sheet.txt")
    def day_sheet(request: Request) -> PlainTextResponse:
        date_param = request.query_params.get("date")
        if date_param is None or not date_param.strip():
            raise HttpError.unprocessable("missing_date", "date query parameter is required")

        statuses_param = request.query_params.get("statuses")
        statuses: tuple[str, ...] | None = None
        if statuses_param:
            statuses = tuple(
                part.strip() for part in statuses_param.split(",") if part.strip()
            )

        try:
            payload = collect_day_sheet(date_param.strip(), include_statuses=statuses)
        except DaySheetDateError as error:
            raise HttpError.unprocessable("invalid_date", str(error)) from error
        except DaySheetNotFoundError as error:
            raise HttpError.not_found("day_sheet_not_found", str(error)) from error

        text = render_day_sheet_ascii(payload)
        return PlainTextResponse(content=text, content_type="text/plain; charset=utf-8")

    @app.get("/api/rosters/crew-roster.csv")
    def crew_roster(request: Request) -> PlainTextResponse:
        date_param = request.query_params.get("date")
        if date_param is None or not date_param.strip():
            raise HttpError.unprocessable("missing_date", "date query parameter is required")

        statuses_param = request.query_params.get("statuses")
        statuses: tuple[str, ...] | None = None
        if statuses_param:
            statuses = tuple(
                part.strip() for part in statuses_param.split(",") if part.strip()
            )

        try:
            payload = collect_roster(date_param.strip(), include_statuses=statuses)
        except RosterDateError as error:
            raise HttpError.unprocessable("invalid_date", str(error)) from error
        except RosterNotFoundError as error:
            raise HttpError.not_found("roster_not_found", str(error)) from error

        csv_text = render_roster_csv(payload)
        return PlainTextResponse(content=csv_text, content_type="text/csv; charset=utf-8")

    @app.get("/api/budgets/budget-variance.txt")
    def budget_variance(request: Request) -> PlainTextResponse:
        threshold_param = request.query_params.get("threshold")
        threshold_value: int | None = None
        if threshold_param is not None and threshold_param.strip():
            try:
                threshold_value = int(threshold_param)
            except ValueError as error:
                raise HttpError.unprocessable("invalid_threshold", "threshold must be an integer") from error

        try:
            payload = collect_budget_variance(alert_threshold=threshold_value)
        except BudgetThresholdError as error:
            raise HttpError.unprocessable("invalid_threshold", str(error)) from error
        except BudgetReportNotFoundError as error:
            raise HttpError.not_found("budget_report_not_found", str(error)) from error

        text = render_budget_variance_ascii(payload)
        return PlainTextResponse(content=text, content_type="text/plain; charset=utf-8")

    @app.get("/api/roles/role-utilization.txt")
    def role_utilization(request: Request) -> PlainTextResponse:
        target_param = request.query_params.get("target")
        target_ratio: float | None = None
        if target_param is not None and target_param.strip():
            try:
                target_value = float(target_param)
            except ValueError as error:
                raise HttpError.unprocessable("invalid_target", "target must be a number") from error
            if target_value <= 0 or target_value > 100:
                raise HttpError.unprocessable("invalid_target", "target must be within 0 and 100")
            target_ratio = target_value / 100.0

        try:
            payload = collect_role_utilization(target_ratio=target_ratio)
        except UtilizationTargetError as error:
            raise HttpError.unprocessable("invalid_target", str(error)) from error
        except UtilizationReportNotFoundError as error:
            raise HttpError.not_found("utilization_report_not_found", str(error)) from error

        text = render_role_utilization_ascii(payload)
        return PlainTextResponse(content=text, content_type="text/plain; charset=utf-8")

    return app


app = create_app()
