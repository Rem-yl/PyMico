from typing import Dict

from api.book import router as book_router
from api.user import router as user_router
from fastapi import FastAPI

app = FastAPI(title="Book API", version="1.0.0")
app.include_router(book_router, prefix="/ch03/api", tags=["books"])
app.include_router(user_router, prefix="/ch03/api", tags=["users"])


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Welcome to the Book API!"}
