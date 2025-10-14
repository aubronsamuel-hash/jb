"""Backend package exposing the dashboard micro API."""
from __future__ import annotations

from .api import app, create_app

__all__ = ["app", "create_app"]
