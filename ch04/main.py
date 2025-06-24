from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from gateway.api_router import router as gateway_router
from loguru import logger
from middleware.exception_handler_middleware import exception_handler_middleware
from student_mgt.student_main import student_app as student_app

app = FastAPI()
app.include_router(gateway_router)
app.mount("/ch04/student", student_app)

logger.add(
    "info.log",
    format="Log: [{extra[log_id]}: {time} - {level} - {message}]",
    level="INFO",
    enqueue=True,
)

app.middleware("http")(exception_handler_middleware)


@app.middleware("http")
async def log_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        logger.info(f"Request to access: {request.url.path}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                f"Request failed with error: {e}, request path: {request.url.path}"
            )
            response = Response(status_code=500, content="Internal Server Error")
        finally:
            logger.info(f"Successfully processed request: {request.url.path}")
    return response


@app.get("/index")
def index() -> Response:
    return Response(content="Hello, World!", media_type="text/plain", status_code=200)
