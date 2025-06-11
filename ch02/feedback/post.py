from __future__ import annotations

from typing import Dict
from uuid import UUID, uuid1

from background import audit_log_transaction
from fastapi import APIRouter, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from handler import PostFeedbackException
from login import approved_users
from places import Post, tours
from pydantic import BaseModel

router = APIRouter()

feedback_tour: Dict[UUID, Assessment] = {}


class Assessment(BaseModel):
    id: UUID
    post: Post
    tour_id: UUID
    tourist_id: UUID


@router.post("/feedback/add")
def post_tourist_feedback(
    tourist_id: UUID, tid: UUID, post: Post, bg_task: BackgroundTasks
) -> JSONResponse:
    if approved_users.get(tourist_id) is None and tours.get(tid) is None:
        raise PostFeedbackException(
            status_code=403, detail="tourist and tour details invalid"
        )

    assess_id = uuid1()
    assessment = Assessment(id=assess_id, post=post, tour_id=tid, tourist_id=tourist_id)
    feedback_tour[assess_id] = assessment
    tours[tid].ratings = (tours[tid].ratings + post.rating) / 2
    bg_task.add_task(
        audit_log_transaction, str(tourist_id), message="post_tourist_feedback"
    )
    assess_json = jsonable_encoder(assessment)
    return JSONResponse(content=assess_json, status_code=200)
