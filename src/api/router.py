# fastapi
from fastapi import APIRouter

# project
from src.api.allocate import router as allocate_router

api_router = APIRouter()
api_router.include_router(allocate_router)
