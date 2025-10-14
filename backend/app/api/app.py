"""Minimal HTTP application used for the Orga dashboard API."""
from __future__ import annotations

import json
from dataclasses import dataclass
from inspect import signature
from typing import Callable, Dict, Iterable, Mapping, Tuple, Union
from urllib.parse import parse_qs

HandlerResponse = Union[Dict[str, object], "PlainTextResponse"]
Handler = Callable[..., HandlerResponse]
RouteKey = Tuple[str, str]


@dataclass(frozen=True)
class Request:
    """Very small request object exposing the query parameters."""

    method: str
    path: str
    query_params: Mapping[str, str]


@dataclass(frozen=True)
class PlainTextResponse:
    """Plain text payload returned by handlers (used for ICS feeds)."""

    content: str
    content_type: str = "text/plain; charset=utf-8"
    status_code: int = 200


class HttpError(Exception):
    """Custom error raised by handlers to signal HTTP level failures."""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message

    @classmethod
    def not_found(cls, code: str, message: str) -> "HttpError":
        return cls(404, code, message)

    @classmethod
    def unprocessable(cls, code: str, message: str) -> "HttpError":
        return cls(422, code, message)

    @classmethod
    def conflict(cls, code: str, message: str) -> "HttpError":
        return cls(409, code, message)

    @classmethod
    def unauthorized(cls, code: str, message: str) -> "HttpError":
        return cls(401, code, message)


class MicroApi:
    """Very small WSGI-compatible application with GET routing only."""

    def __init__(self, title: str, version: str) -> None:
        self.title = title
        self.version = version
        self._routes: Dict[RouteKey, Handler] = {}

    def get(self, path: str) -> Callable[[Handler], Handler]:
        """Register a GET handler for the given path."""

        normalized = path if path.startswith("/") else f"/{path}"

        def decorator(handler: Handler) -> Handler:
            self._routes[("GET", normalized)] = handler
            return handler

        return decorator

    def dispatch(self, method: str, path: str) -> Tuple[int, HandlerResponse]:
        """Return status code and payload for the route."""

        normalized_method = method.upper()
        plain_path, _, query_string = path.partition("?")
        handler = self._routes.get((normalized_method, plain_path))
        if handler is None:
            return 404, {"error": {"code": "route_not_found", "message": "Route not found"}}

        raw_params = parse_qs(query_string, keep_blank_values=True)
        query_params = {key: values[-1] if values else "" for key, values in raw_params.items()}
        request = Request(method=normalized_method, path=plain_path, query_params=query_params)

        try:
            payload = self._call_handler(handler, request)
        except HttpError as error:
            return error.status_code, {"error": {"code": error.code, "message": error.message}}

        if isinstance(payload, PlainTextResponse):
            return payload.status_code, payload
        if not isinstance(payload, dict):
            raise TypeError("Handlers must return dictionaries or PlainTextResponse")
        return 200, payload

    def _call_handler(self, handler: Handler, request: Request) -> HandlerResponse:
        """Call the handler with the minimal request context if requested."""

        parameters = signature(handler).parameters
        if not parameters:
            return handler()  # type: ignore[return-value]
        return handler(request)

    def __call__(self, environ: Dict[str, object], start_response: Callable[[str, Iterable[Tuple[str, str]]], None]):
        method = str(environ.get("REQUEST_METHOD", "GET")).upper()
        path = str(environ.get("PATH_INFO", "/"))
        status_code, payload = self.dispatch(method, path)
        if isinstance(payload, PlainTextResponse):
            body = payload.content.encode("utf-8")
            headers = [
                ("Content-Type", payload.content_type),
                ("Content-Length", str(len(body))),
                ("X-Orga-Api", self.version),
            ]
        else:
            body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
            headers = [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Content-Length", str(len(body))),
                ("X-Orga-Api", self.version),
            ]
        status_phrase = self._status_phrase(status_code)
        start_response(f"{status_code} {status_phrase}", headers)
        return [body]

    @staticmethod
    def _status_phrase(status_code: int) -> str:
        mapping = {
            200: "OK",
            401: "Unauthorized",
            404: "Not Found",
            409: "Conflict",
            422: "Unprocessable Entity",
        }
        return mapping.get(status_code, "OK")


__all__ = ["HttpError", "MicroApi", "PlainTextResponse", "Request"]
