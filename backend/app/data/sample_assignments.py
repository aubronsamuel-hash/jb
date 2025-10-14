"""Deterministic assignments used for QA pagination scenarios."""
from __future__ import annotations

from typing import Tuple

from ..models.planning import Assignment


def load_sample_assignments() -> Tuple[Assignment, ...]:
    """Return a stable set of assignments sorted by update time desc."""

    return (
        Assignment(
            id="asg-aurora-light-1",
            mission_id="m-light-tech",
            mission_title="Balance lumiere",
            user_id="crew-malik",
            user_name="Malik Roche",
            role="lumiere",
            status="confirmed",
            starts_at="2024-06-10T08:00:00Z",
            ends_at="2024-06-10T14:00:00Z",
            updated_at="2024-05-06T07:35:00Z",
            location="Grande scene",
        ),
        Assignment(
            id="asg-aurora-sound-1",
            mission_id="m-soundcheck",
            mission_title="Soundcheck groupe A",
            user_id="crew-sonia",
            user_name="Sonia Lefevre",
            role="son",
            status="in-progress",
            starts_at="2024-06-11T07:00:00Z",
            ends_at="2024-06-11T11:00:00Z",
            updated_at="2024-05-06T07:10:00Z",
            location="Studio B",
        ),
        Assignment(
            id="asg-riverside-video-1",
            mission_id="m-video-calibration",
            mission_title="Calibration cameras",
            user_id="crew-ines",
            user_name="Ines Martel",
            role="video",
            status="pending",
            starts_at="2024-07-04T10:00:00Z",
            ends_at="2024-07-04T15:00:00Z",
            updated_at="2024-05-05T18:40:00Z",
            location="Salle capture",
        ),
        Assignment(
            id="asg-riverside-plateau-1",
            mission_id="m-stage-management",
            mission_title="Coordination plateau",
            user_id="crew-jules",
            user_name="Jules Pinto",
            role="plateau",
            status="planned",
            starts_at="2024-07-05T09:00:00Z",
            ends_at="2024-07-05T12:00:00Z",
            updated_at="2024-05-05T11:25:00Z",
            location="Backstage",
        ),
        Assignment(
            id="asg-aurora-light-2",
            mission_id="m-light-tech",
            mission_title="Balance lumiere",
            user_id="crew-ines",
            user_name="Ines Martel",
            role="video",
            status="declined",
            starts_at="2024-06-10T08:00:00Z",
            ends_at="2024-06-10T14:00:00Z",
            updated_at="2024-05-04T19:05:00Z",
            location="Grande scene",
        ),
    )


__all__ = ["load_sample_assignments"]
