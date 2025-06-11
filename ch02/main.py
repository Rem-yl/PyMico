import login
import places
import tourist
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from handler import PostFeedbackException, PostRatingException

app = FastAPI()

app.include_router(login.router)
app.include_router(places.router)
app.include_router(tourist.router)


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
