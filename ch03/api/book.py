from typing import Annotated

from database import BookDatabase, get_book_db
from dependencies import admin_required
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from model import User

router = APIRouter()


@router.get("/books/list")
def list_books(db: Annotated[BookDatabase, Depends(get_book_db)]) -> JSONResponse:
    try:
        json_str = jsonable_encoder(db.list_books())
        msg = {
            "message": "Books retrieved successfully",
            "data": json_str,
            "error": None,
        }

        return JSONResponse(content=msg, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"server error: {str(e)}") from e


@router.post("/books/add")
def add_book(
    name: str,
    author: str,
    db: Annotated[BookDatabase, Depends(get_book_db)],
    _: Annotated[User, Depends(admin_required)],
) -> JSONResponse:
    try:
        db.add_book(name, author)
        msg = {
            "message": "Book added successfully",
            "data": None,
            "error": None,
        }
        return JSONResponse(content=msg, status_code=201)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding book: {str(e)}"
        ) from e


@router.delete("/books/delete")
def delete_book(
    name: str,
    db: Annotated[BookDatabase, Depends(get_book_db)],
    _: Annotated[User, Depends(admin_required)],
) -> JSONResponse:
    try:
        db.delete_book(name)
        msg = {
            "message": "Book deleted successfully",
            "data": None,
            "error": None,
        }

        return JSONResponse(content=msg, status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting book: {str(e)}"
        ) from e
