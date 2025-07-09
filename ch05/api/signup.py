from typing import Annotated, Generator, List, Optional, Union

from database import SessionFactory
from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from models.data.signup import Member, SignUp, Trainer
from models.req.signup import (
    MemberOut,
    SignUpOut,
    SignUpReq,
    TrainerOut,
    UserReq,
    UserType,
)
from repo.signup import MemberSignupRepo, SignUpRepo, TrainerSignupRepo
from sqlalchemy.orm import Session

router = APIRouter()


def build_next_url(request: Request, relative_path: str) -> str:
    path_prefix = request.url.path.split("/")[1]
    return f"/{path_prefix}{relative_path}"


def sess_db() -> Generator[Session, None, None]:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.get("/signup/unknown", response_model=None)
def signup_root() -> JSONResponse:
    return JSONResponse(content={"message": "Signup API"}, status_code=201)


@router.post("/signup/add", response_model=None)
def add_signup(
    request: Request,
    req: SignUpReq,
    sess: Annotated[Session, Depends(sess_db)],
) -> Union[RedirectResponse, JSONResponse]:
    repo: SignUpRepo = SignUpRepo(sess)
    model = SignUp(username=req.username, password=req.password, user_type=req.usertype)
    model = repo.add(model)

    if model is not None:
        signup_id = model.id

        if req.usertype == UserType.MEMBER:
            next_url = f"/signup/member/add?signup_id={signup_id}"
        elif req.usertype == UserType.TRAINER:
            next_url = f"/signup/trainer/add?signup_id={signup_id}"
        else:
            next_url = "/signup/unknown"

        next_url = build_next_url(request, next_url)

        return RedirectResponse(url=next_url, status_code=303)

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


@router.get("/signup/list")
def list_signups(sess: Annotated[Session, Depends(sess_db)]) -> JSONResponse:
    repo: SignUpRepo = SignUpRepo(sess)

    orm_list: List[SignUp] = repo.list_signups()

    # 手动转换为 Pydantic 模型，再转成 dict
    data = [SignUpOut.from_orm(obj) for obj in orm_list]

    return JSONResponse(content=jsonable_encoder(data), status_code=200)


@router.get("/signup/member/add", response_class=HTMLResponse)
def get_member_form(signup_id: int = Query(...)) -> HTMLResponse:
    html_content = f"""
    <html>
        <head><title>Complete Member Info</title></head>
        <body>
            <h2>Complete Info for signup_id={signup_id}</h2>
            <form action="/ch05/signup/member/add" method="post">
                <input type="hidden" name="signup_id" value="{signup_id}" />
                Age: <input type="number" name="age" /><br/>
                Level: <input type="text" name="level" /><br/>
                Gender: <input type="text" name="gender" /><br/>
                <input type="submit" value="Submit" />
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/signup/trainer/add", response_class=HTMLResponse)
def get_trainer_form(signup_id: int = Query(...)) -> HTMLResponse:
    html_content = f"""
    <html>
        <head><title>Complete Trainer Info</title></head>
        <body>
            <h2>Complete Info for signup_id={signup_id}</h2>
            <form action="/ch05/signup/trainer/add" method="post">
                <input type="hidden" name="signup_id" value="{signup_id}" />
                Age: <input type="number" name="age" /><br/>
                Level: <input type="text" name="level" /><br/>
                Gender: <input type="text" name="gender" /><br/>
                Height: <input type="number" name="height" /><br/>
                Weight: <input type="number" name="weight" /><br/>
                <input type="submit" value="Submit" />
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.post("/signup/member/add")
def add_member(
    sess: Annotated[Session, Depends(sess_db)],
    signup_id: int = Form(...),
    trainer_id: Optional[int] = Form(None),
    age: int = Form(...),
    level: int = Form(...),
    gender: int = Form(...),
) -> JSONResponse:
    repo = MemberSignupRepo(sess)
    model = Member(
        signup_id=signup_id,
        trainer_id=trainer_id,
        age=age,
        level=level,
        gender=gender,
    )
    success = repo.add(model)

    if success:
        return JSONResponse(
            content={
                "message": "MemberSignUp successful",
                "data": {},
            },
            status_code=201,
        )

    return JSONResponse(
        content={
            "message": "MemberSignUp failed",
            "data": {},
        },
        status_code=500,
    )


@router.get("/signup/member/list")
def list_members(sess: Annotated[Session, Depends(sess_db)]) -> JSONResponse:
    repo = MemberSignupRepo(sess)
    members: List[Member] = repo.list_members()

    data = [MemberOut.from_orm(obj) for obj in members]

    return JSONResponse(content=jsonable_encoder(data), status_code=200)


@router.post("/signup/trainer/add")
def add_trainer(
    sess: Annotated[Session, Depends(sess_db)],
    signup_id: int = Form(...),
    age: int = Form(...),
    level: int = Form(...),
    gender: int = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
) -> JSONResponse:
    repo = TrainerSignupRepo(sess)
    model = Trainer(
        signup_id=signup_id,
        age=age,
        level=level,
        gender=gender,
        height=height,
        weight=weight,
    )
    success = repo.add(model)

    if success:
        return JSONResponse(
            content={
                "message": "TrainerSignUp successful",
                "data": {},
            },
            status_code=201,
        )

    return JSONResponse(
        content={
            "message": "TrainerSignUp failed",
            "data": {},
        },
        status_code=500,
    )


@router.get("/signup/trainer/list")
def list_trainers(sess: Annotated[Session, Depends(sess_db)]) -> JSONResponse:
    repo = TrainerSignupRepo(sess)
    trainers: List[Trainer] = repo.list_trainers()

    data = [TrainerOut.from_orm(obj) for obj in trainers]

    return JSONResponse(content=jsonable_encoder(data), status_code=200)
