from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from student_mgt.models.student import Login, Signup, SignupReq, Student, StudentReq
from student_mgt.services.student import (
    StudentLoginService,
    StudentService,
    StudentSignupService,
    get_student_login_service,
    get_student_service,
    get_student_signup_service,
)

router = APIRouter()


@router.post("/account/signup")
def signup(
    signup: SignupReq,
    service: Annotated[StudentSignupService, Depends(get_student_signup_service)],
) -> JSONResponse:

    account = Signup(
        id=uuid4(),
        username=signup.username,
        password=signup.password,
        is_admin=signup.is_admin,
    )
    service.add(account)

    return JSONResponse(
        content={
            "message": f"Student {signup.username} signed up successfully",
            "data": {},
        },
        status_code=201,
    )


@router.get("/account/signup/approved")
def approved_signup(
    uname: str,
    signup_service: Annotated[
        StudentSignupService, Depends(get_student_signup_service)
    ],
    login_service: Annotated[StudentLoginService, Depends(get_student_login_service)],
) -> JSONResponse:
    account = signup_service.get(uname)

    if account:
        login = Login(**account.model_dump())
        login_service.add(login)
        signup_service.remove(uname)
        return JSONResponse(
            content={
                "message": f"Student {uname} signup approved",
                "data": jsonable_encoder(login),
            },
            status_code=200,
        )
    else:
        return JSONResponse(
            content={"message": f"Student {uname} not found"}, status_code=404
        )


@router.post("/login/password/change")
def change_password(
    username: str,
    old_password: str,
    new_password: str,
    login_service: Annotated[StudentLoginService, Depends(get_student_login_service)],
) -> JSONResponse:
    login = login_service.get(username)

    if login.password != old_password:
        return JSONResponse(
            content={"message": "Old password does not match"}, status_code=400
        )

    login_service.update_password(username, new_password)

    return JSONResponse(
        content={"message": "Password changed successfully"}, status_code=200
    )


@router.post("/profile/add")
def create_profile(
    profile: StudentReq,
    service: Annotated[StudentService, Depends(get_student_service)],
) -> JSONResponse:
    student = Student(id=uuid4(), name=profile.name, age=profile.age)
    service.add(student)

    return JSONResponse(
        content={
            "message": f"Student {profile.name} created successfully",
            "data": jsonable_encoder(student),
        },
        status_code=201,
    )


@router.patch("/profile/update")
def update_profile(
    new_profile: StudentReq,
    service: Annotated[StudentService, Depends(get_student_service)],
) -> JSONResponse:
    service.update(new_profile)

    return JSONResponse(
        content={
            "message": f"Student {new_profile.name} updated successfully",
            "data": jsonable_encoder(new_profile),
        },
        status_code=200,
    )
