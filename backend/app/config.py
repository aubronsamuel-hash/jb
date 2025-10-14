"""Configuration constants shared across the backend services."""

API_TITLE = "Orga Dashboard API"
API_VERSION = "0.2.0"


def get_api_metadata() -> dict[str, str]:
    """Return the basic metadata exposed by the API surface."""

    return {"title": API_TITLE, "version": API_VERSION}


__all__ = ["API_TITLE", "API_VERSION", "get_api_metadata"]
