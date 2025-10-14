"""Minimal HTTP application used for the Orga dashboard API."""
from __future__ import annotations

import json
from typing import Callable, Dict, Iterable, Tuple

Handler = Callable[[], Dict[str, object]]
RouteKey = Tuple[str, str]


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

    def dispatch(self, method: str, path: str) -> Tuple[int, Dict[str, object]]:
        """Return status code and payload for the route."""

        key = (method.upper(), path)
        handler = self._routes.get(key)
        if handler is None:
            return 404, {"error": "Not Found"}
        payload = handler()
        if not isinstance(payload, dict):
            raise TypeError("Handlers must return dictionaries")
        return 200, payload

    def __call__(self, environ: Dict[str, object], start_response: Callable[[str, Iterable[Tuple[str, str]]], None]):
        method = str(environ.get("REQUEST_METHOD", "GET")).upper()
        path = str(environ.get("PATH_INFO", "/"))
        status_code, payload = self.dispatch(method, path)
        body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        status_phrase = "OK" if status_code == 200 else "Not Found"
        headers = [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("X-Orga-Api", self.version),
        ]
        start_response(f"{status_code} {status_phrase}", headers)
        return [body]


__all__ = ["MicroApi"]
