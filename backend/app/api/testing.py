"""Test helpers for exercising the MicroApi."""
from __future__ import annotations

import json
from dataclasses import dataclass

from .app import MicroApi, PlainTextResponse


@dataclass
class ApiResponse:
    status_code: int
    body: str
    content_type: str

    def json(self) -> dict[str, object]:
        if "application/json" not in self.content_type:
            raise ValueError("Response is not JSON")
        return json.loads(self.body)

    @property
    def text(self) -> str:
        return self.body


class ApiTestClient:
    """Simple synchronous client that calls the micro API directly."""

    def __init__(self, app: MicroApi) -> None:
        self._app = app

    def get(self, path: str) -> ApiResponse:
        status_code, payload = self._app.dispatch("GET", path)
        if isinstance(payload, PlainTextResponse):
            return ApiResponse(
                status_code=status_code,
                body=payload.content,
                content_type=payload.content_type,
            )
        body = json.dumps(payload, ensure_ascii=True)
        return ApiResponse(
            status_code=status_code,
            body=body,
            content_type="application/json; charset=utf-8",
        )


__all__ = ["ApiResponse", "ApiTestClient"]
