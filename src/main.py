# fastapi
from fastapi import FastAPI

# project
from src.api.router import api_router

app = FastAPI()
app.include_router(router=api_router, prefix="/api")
