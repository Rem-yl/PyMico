from typing import Dict

from api.signup import router as signup_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(signup_router, prefix="/ch05", tags=["signup"])


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "健身房会员登录系统"}
