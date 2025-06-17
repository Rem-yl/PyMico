from typing import Annotated

from database import BookDatabase, get_book_db
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

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
    except Exception as e:
        msg = {
            "message": "Error retrieving books",
            "data": None,
            "error": str(e),
        }

    return JSONResponse(content=msg, status_code=200)


@router.post("/books/add")
def add_book(
    name: str, author: str, db: Annotated[BookDatabase, Depends(get_book_db)]
) -> JSONResponse:
    try:
        db.add_book(name, author)
        msg = {
            "message": "Book added successfully",
            "data": None,
            "error": None,
        }
    except Exception as e:
        msg = {
            "message": "Error adding book",
            "data": None,
            "error": str(e),
        }

    return JSONResponse(content=msg, status_code=201)


@router.delete("/books/delete")
def delete_book(
    name: str, db: Annotated[BookDatabase, Depends(get_book_db)]
) -> JSONResponse:
    try:
        db.delete_book(name)
        msg = {
            "message": "Book deleted successfully",
            "data": None,
            "error": None,
        }
    except Exception as e:
        msg = {
            "message": "Error deleting book",
            "data": None,
            "error": str(e),
        }

    return JSONResponse(content=msg, status_code=200)
