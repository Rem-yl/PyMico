from __future__ import annotations

from datetime import datetime
from typing import Dict, List
from uuid import UUID, uuid1

from background import audit_log_transaction
from fastapi import APIRouter, BackgroundTasks, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from places import TourBasicInfo
from pydantic import BaseModel

router = APIRouter()

pending_users: Dict[UUID, Tourist] = {}
approved_users: Dict[UUID, Tourist] = {}


class Signup(BaseModel):
    username: str
    password: str
    birthday: datetime


class User(BaseModel):
    id: UUID
    username: str
    password: str


class Tourist(BaseModel):
    id: UUID
    login: User
    date_signed: datetime
    booked: int
    tours: List[TourBasicInfo]


@router.post("/ch02/user/signup/")
def signup(signup: Signup) -> JSONResponse:
    try:
        userid = uuid1()
        login = User(id=userid, username=signup.username, password=signup.password)
        tourist = Tourist(
            id=userid,
            login=login,
            date_signed=datetime.now(),
            booked=0,
            tours=[],
        )
        tourist_json = jsonable_encoder(tourist)
        pending_users[userid] = tourist
        return JSONResponse(content=tourist_json, status_code=status.HTTP_201_CREATED)
    except Exception as _:
        return JSONResponse(
            content={"message": "invalid operation"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/ch02/user/login")
def login(login: User, bg_task: BackgroundTasks) -> JSONResponse:
    try:
        signup_json = jsonable_encoder(approved_users[login.id])
        bg_task.add_task(
            audit_log_transaction, tourist_id=str(login.id), message="login"
        )

        return JSONResponse(content=signup_json, status_code=status.HTTP_200_OK)
    except Exception as _:
        return JSONResponse(
            content={"message": "invalid operation"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
