from datetime import datetime
from typing import Awaitable, Callable

import feedback
import login
import places
import tourist
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from handler import PostFeedbackException, PostRatingException
from starlette.exceptions import HTTPException as GlobalStarletteHTTPException

app = FastAPI()

app.include_router(login.router)
app.include_router(places.router)
app.include_router(tourist.router)
app.include_router(feedback.router)


# app.exception_handler 注册为全局异常处理器, 当代码抛出这些异常时, fastapi会自动调用对应的处理函数
@app.exception_handler(PostFeedbackException)
def feedback_exception_handler(req: Request, ex: PostFeedbackException) -> JSONResponse:
    return JSONResponse(
        status_code=ex.status_code, content={"message": f"error: {ex.detail}"}
    )


@app.exception_handler(PostRatingException)
def rating_exception_handler(req: Request, ex: PostRatingException) -> JSONResponse:
    return JSONResponse(
        status_code=ex.status_code, content={"message": f"error: {ex.detail}"}
    )


@app.exception_handler(GlobalStarletteHTTPException)
def global_exception_handler(
    req: Request, ex: GlobalStarletteHTTPException
) -> PlainTextResponse:
    return PlainTextResponse(f"Error message: {ex.detail}", status_code=ex.status_code)


@app.exception_handler(RequestValidationError)
def validation_exception_hander(
    req: Request, ex: RequestValidationError
) -> PlainTextResponse:
    return PlainTextResponse(f"Error message: {str(ex)}", status_code=400)


@app.middleware("http")
async def log_transaction_filter(
    req: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = datetime.now()
    method_name = req.method
    qp_map = req.query_params
    pp_map = req.path_params

    with open("request.log", mode="a", encoding="utf-8") as f:
        content = f"method: {method_name}, query param: {qp_map}, path params: {pp_map} received at {datetime.now()}\n"
        f.write(content)

    response = await call_next(req)
    process_time = datetime.now() - start_time
    response.headers["X-Time-Elapsed"] = str(process_time)

    return response
