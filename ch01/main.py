from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/ch01/index")
def index() -> Dict[str, str]:
    return {"message": "Welcome FastAPI"}
