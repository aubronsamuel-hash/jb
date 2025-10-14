from __future__ import annotations

import json
from dataclasses import dataclass

from .app import MicroApi


@dataclass
class ApiResponse:
    status_code: int
    _payload: dict[str, object]

    def json(self) -> dict[str, object]:
        return self._payload

    @property
    def text(self) -> str:
        return json.dumps(self._payload, ensure_ascii=True)


class ApiTestClient:
    """Simple synchronous client that calls the micro API directly."""

    def __init__(self, app: MicroApi) -> None:
        self._app = app

    def get(self, path: str) -> ApiResponse:
        status_code, payload = self._app.dispatch("GET", path)
        return ApiResponse(status_code=status_code, _payload=payload)


__all__ = ["ApiResponse", "ApiTestClient"]
