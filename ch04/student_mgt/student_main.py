from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse
from student_mgt.controllers.admin import router as admin_router
from student_mgt.controllers.assignments import router as assignments_router
from student_mgt.controllers.reservations import router as reservations_router

student_app = FastAPI(
    title="Student Management System",
    description="API for managing student data",
    version="1.0.0",
)
student_app.include_router(
    reservations_router, prefix="/reservations", tags=["reservations"]
)
student_app.include_router(admin_router, prefix="/admin", tags=["admin"])
student_app.include_router(
    assignments_router, prefix="/assignments", tags=["assignments"]
)


@student_app.get("/docs", include_in_schema=False)
async def student_docs() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Student API Docs")


@student_app.get("/index")
def student_index() -> JSONResponse:
    return JSONResponse(
        content={"message": "Welcome to the Student Management System!"},
        status_code=200,
    )
