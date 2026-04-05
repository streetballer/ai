from fastapi import APIRouter
from src.common.controllers.health_check import router as health_check_router

router = APIRouter()

router.include_router(health_check_router)
