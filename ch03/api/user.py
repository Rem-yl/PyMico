from typing import Annotated

from database import UserDatabase, get_user_db
from fastapi import APIRouter, Depends, HTTPException
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

        return JSONResponse(content=msg, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e


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

        return JSONResponse(content=msg, status_code=201)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding user: {str(e)}"
        ) from e


@router.delete("/users/delete")
def delete_user(
    username: str,
    db: Annotated[UserDatabase, Depends(get_user_db)],
) -> JSONResponse:
    try:
        db.delete_user(username)
        msg = {
            "message": "User deleted successfully",
            "data": None,
            "error": None,
        }

        return JSONResponse(content=msg, status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting user: {str(e)}"
        ) from e
