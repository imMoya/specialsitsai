from fastapi import APIRouter
from app.api.endpoints import oddlots, spinoffs

api_router = APIRouter()
api_router.include_router(oddlots.router, prefix="/oddlots", tags=["oddlots"])
api_router.include_router(spinoffs.router, prefix="/spinoffs", tags=["spinoffs"])