"""API package exposing the dashboard micro API factory."""
from __future__ import annotations

from .main import app, create_app

__all__ = ["app", "create_app"]
