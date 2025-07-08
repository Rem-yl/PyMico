from typing import Annotated, Generator

from database import SessionFactory
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.data.signup import SignUp
from models.req.signup import SignUpReq, UserReq
from repo.signup import SignUpRepo
from sqlalchemy.orm import Session

router = APIRouter()


def sess_db() -> Generator[Session, None, None]:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup/add")
def add_signup(
    req: SignUpReq, sess: Annotated[Session, Depends(sess_db)]
) -> JSONResponse:
    repo: SignUpRepo = SignUpRepo(sess)
    model = SignUp(username=req.username, password=req.password, user_type=req.usertype)
    success = repo.add(model)

    if success:
        return JSONResponse(
            content={
                "message": f"Signup successful for user: {req.username}",
                "data": {},
            },
            status_code=201,
        )

    return JSONResponse(
        content={
            "message": f"Signup failed for user: {req.username}",
            "data": {},
        },
        status_code=500,
    )


@router.post("/signup/update")
def update_signup(
    req: UserReq, new_req: SignUpReq, sess: Annotated[Session, Depends(sess_db)]
) -> JSONResponse:
    repo: SignUpRepo = SignUpRepo(sess)
    model = SignUp(username=req.username, password=req.password)
    new_model = SignUp(
        username=req.username, password=new_req.password, user_type=new_req.usertype
    )
    success = repo.update(model, new_model)

    if success:
        return JSONResponse(
            content={
                "message": f"Update successful for user: {req.username}",
                "data": {},
            },
            status_code=201,
        )

    return JSONResponse(
        content={
            "message": f"Update failed for user: {req.username}",
            "data": {},
        },
        status_code=500,
    )


@router.post("/signup/delete")
def delete_signup(
    req: UserReq, sess: Annotated[Session, Depends(sess_db)]
) -> JSONResponse:
    repo: SignUpRepo = SignUpRepo(sess)
    success = repo.delete(req.username, req.password)

    if success:
        return JSONResponse(
            content={
                "message": f"Delete successful for user: {req.username}",
                "data": {},
            },
            status_code=201,
        )

    return JSONResponse(
        content={
            "message": f"Delete failed for user: {req.username}",
            "data": {},
        },
        status_code=500,
    )
