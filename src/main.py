# stdlib
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

# fastapi
from fastapi import FastAPI

# project
from src.api.router import api_router
from src.db.db import setup_db
from src.models.orm_models import start_mappers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    setup_db(app)
    start_mappers()
    yield
    await app.state.db_engine.dispose()


fastapi_app = FastAPI(lifespan=lifespan)
fastapi_app.include_router(router=api_router, prefix="/api")
