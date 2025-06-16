from __future__ import annotations

from typing import Dict
from uuid import UUID, uuid1

from background import audit_log_transaction
from fastapi import APIRouter, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from handler import PostFeedbackException, PostRatingException
from login import approved_users
from places import Post, StarRating, tours
from pydantic import BaseModel
from utils import check_post_owner

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


@router.post("/feedback/update/rating")
def update_tour_rating(assess_id: UUID, new_rating: StarRating) -> JSONResponse:
    if feedback_tour.get(assess_id) is None:
        raise PostRatingException(status_code=403, detail="tour assessment invalid")

    tid = feedback_tour[assess_id].tour_id
    tours[tid].ratings = (tours[tid].ratings + new_rating) / 2
    tour_json = jsonable_encoder(tours[tid])

    return JSONResponse(content=tour_json, status_code=200)


@router.get("/feedback/list")
async def show_tourist_post(tourist_id: UUID) -> JSONResponse:
    tourist_posts = [
        assess for assess in feedback_tour.values() if assess.tour_id == tourist_id
    ]
    tourist_posts_json = jsonable_encoder(tourist_posts)

    return JSONResponse(content=tourist_posts_json, status_code=200)


@router.delete("/feedback/delete")
async def delete_tourist_feedback(assess_id: UUID, tourist_id: UUID) -> JSONResponse:
    if approved_users.get(tourist_id) is None and feedback_tour.get(assess_id):
        raise PostFeedbackException(
            detail="tourist and tour details invalid", status_code=403
        )

    post_delete = [
        access for access in feedback_tour.values() if access.id == assess_id
    ]

    for key in post_delete:
        is_owner = await check_post_owner(feedback_tour, assess_id, tourist_id)
        if is_owner:
            del feedback_tour[key.id]

    return JSONResponse(
        content={"message": f"deleted posts of {tourist_id}"}, status_code=200
    )
