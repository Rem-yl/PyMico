from __future__ import annotations

from typing import Any, Dict
from uuid import UUID

from feedback import Assessment


async def check_post_owner(
    feedbacks: Dict[UUID, Assessment], fid: UUID, tourist_id: UUID
) -> Any:
    feedback: Assessment = feedbacks[fid]
    return feedback.tourist_id == tourist_id
