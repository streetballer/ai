from fastapi import APIRouter
from src.modules.auth.controllers.refresh import router as refresh_router

router = APIRouter()

router.include_router(refresh_router)
