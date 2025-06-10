import login
import places
from fastapi import FastAPI

app = FastAPI()

app.include_router(login.router)
app.include_router(places.router)
