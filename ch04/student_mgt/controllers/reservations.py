from json import dumps

import httpx
from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from student_mgt.models.library_req import BookIssuanceReq

router = APIRouter()


@router.get("/access/book")
def access_book(request: Request) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")
    url = f"{base_url}/ch04/library/book/list"

    with httpx.Client() as client:
        try:
            response = client.get(url)
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                content={
                    "error": "Failed to access book list",
                    "details": str(exc),
                },
                status_code=500,
            )


@router.post("/reserve/book")
def reserve_book(request: Request, book: BookIssuanceReq) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")
    url = f"{base_url}/ch04/library/book/issuance"

    with httpx.Client() as client:
        try:
            response = client.post(url, data={"book": dumps(jsonable_encoder(book))})
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                content={
                    "error": "Failed to reserve book",
                    "details": str(exc),
                },
                status_code=500,
            )

    return response
