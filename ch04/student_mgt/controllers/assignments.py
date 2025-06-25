import httpx
from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from student_mgt.models.student import AssignmentRequest

router = APIRouter()


@router.get("/assignments/list")
def list_assignments(request: Request) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")
    url = f"{base_url}/ch04/assignments/list"

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
                    "error": "Failed to access assignments list",
                    "details": str(exc),
                },
                status_code=500,
            )


@router.post("/assignments/submit")
def submit_assignment(request: Request, assignment: AssignmentRequest) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")
    url = f"{base_url}/ch04/assignments/submit"

    with httpx.Client() as client:
        try:
            response = client.post(
                url,
                json=jsonable_encoder(assignment),
                headers={"Content-Type": "application/json"},
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                content={
                    "error": "Failed to submit assignment",
                    "details": str(exc),
                },
                status_code=500,
            )
