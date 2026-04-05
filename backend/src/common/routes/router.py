from fastapi import APIRouter
from src.common.controllers.health_check import router as health_check_router
from src.modules.auth.routes.router import router as auth_router

router = APIRouter()

router.include_router(health_check_router)
router.include_router(auth_router)
