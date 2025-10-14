from __future__ import annotations

import pytest

from backend.app.services.planning import (
    AssignmentCursorNotFound,
    AssignmentPaginationError,
    get_assignment_feed,
)


def test_feed_returns_expected_structure() -> None:
    feed = get_assignment_feed(cursor=None, limit=3)
    assert feed["pageInfo"]["nextCursor"] == "asg-riverside-video-1"
    assert feed["summary"]["byStatus"]["confirmed"] == 1
    assert feed["items"][0]["user"]["name"] == "Malik Roche"


def test_feed_raises_on_invalid_limit() -> None:
    with pytest.raises(AssignmentPaginationError):
        get_assignment_feed(cursor=None, limit=0)


def test_feed_raises_on_unknown_cursor() -> None:
    with pytest.raises(AssignmentCursorNotFound):
        get_assignment_feed(cursor="does-not-exist", limit=2)
