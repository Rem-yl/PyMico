from typing import Annotated

from database import UserDatabase, get_user_db
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from model import UserOut

router = APIRouter()


@router.get("/users/list", response_model=UserOut)
def list_users(db: Annotated[UserDatabase, Depends(get_user_db)]) -> JSONResponse:
    try:
        users_out = [
            user.model_dump(exclude={"password"}) for user in db.users.values()
        ]

        msg = {
            "message": "Users retrieved successfully",
            "data": jsonable_encoder(users_out),
            "error": None,
        }
    except Exception as e:
        msg = {
            "message": "Error retrieving users",
            "data": None,
            "error": str(e),
        }

    return JSONResponse(content=msg, status_code=200)


@router.post("/users/add")
def add_user(
    username: str, password: str, db: Annotated[UserDatabase, Depends(get_user_db)]
) -> JSONResponse:
    try:
        db.add_user(username, password)
        msg = {
            "message": "User added successfully",
            "data": None,
            "error": None,
        }
    except Exception as e:
        msg = {
            "message": "Error adding user",
            "data": None,
            "error": str(e),
        }

    return JSONResponse(content=msg, status_code=201)


@router.delete("/users/delete")
def delete_user(
    username: str, db: Annotated[UserDatabase, Depends(get_user_db)]
) -> JSONResponse:
    try:
        db.delete_user(username)
        msg = {
            "message": "User deleted successfully",
            "data": None,
            "error": None,
        }
    except Exception as e:
        msg = {
            "message": "Error deleting user",
            "data": None,
            "error": str(e),
        }

    return JSONResponse(content=msg, status_code=200)
