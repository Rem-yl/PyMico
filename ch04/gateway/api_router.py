from typing import Union

from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/ch04",
    tags=["gateway"],
)


@router.get("/{portal_id}")
async def handle_portal(portal_id: str) -> Union[RedirectResponse, Response]:
    """
    Handles requests to the API gateway and redirects based on the portal_id.
    """
    if portal_id == "1":
        return RedirectResponse(url="/ch04/student/index", status_code=302)
    elif portal_id == "2":
        return RedirectResponse(url="/ch04/faculty/index", status_code=302)
    elif portal_id == "3":
        return RedirectResponse(url="/ch04/library/index", status_code=302)
    else:
        return Response(status_code=404, content=f"Portal id: {portal_id} not found")
