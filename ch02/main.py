import login
import places
import tourist
from fastapi import FastAPI

app = FastAPI()

app.include_router(login.router)
app.include_router(places.router)
app.include_router(tourist.router)
