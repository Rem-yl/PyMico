# exception_handler_middleware.py

import traceback
from typing import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from loguru import logger

logger.add(
    "info.log",
    format="Log: [{extra[log_id]}: {time} - {level} - {message}]",
    level="INFO",
    enqueue=True,
)


async def exception_handler_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    try:
        return await call_next(request)
    except Exception as exc:
        # 手动提取 traceback 文字
        tb_text = traceback.format_exc()

        # 打印日志，包括 traceback
        logger.error(f"❌ Unhandled exception for {request.url.path}:\n{tb_text}")

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(exc),
                "path": request.url.path,
            },
        )
