"""Sample tokens used to secure calendar ICS feeds for Step 14."""
from __future__ import annotations

from typing import Dict


def load_calendar_tokens() -> Dict[str, str]:
    """Return deterministic token mapping for demo calendar feeds."""

    return {
        "ALL": "ics-demo-scope-all",
        "USER:crew-malik": "ics-demo-user-crew-malik",
        "USER:crew-ines": "ics-demo-user-crew-ines",
        "PROJECT:m-light-tech": "ics-demo-project-light",
    }


__all__ = ["load_calendar_tokens"]
