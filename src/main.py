from fastapi import FastAPI
from src.database.database import init_db
from src.api.controller import router as api_route
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

def registered_routes():
    app.include_router(api_route)

registered_routes()