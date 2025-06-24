from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/access/book")
def access_book(request: Request) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")

    response = JSONResponse(
        content={
            "message": "TODO: Accessing book list from the library service",
            "base_url": base_url,
        },
        status_code=200,
    )

    return response


@router.post("/reserve/book")
def reserve_book(request: Request) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")

    response = JSONResponse(
        content={
            "message": "TODO: Reserving book from the library service",
            "base_url": base_url,
        },
        status_code=200,
    )

    return response
