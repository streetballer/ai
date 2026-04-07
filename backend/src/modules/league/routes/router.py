from fastapi import APIRouter
from src.modules.league.controllers.get_league import router as get_league_router

router = APIRouter()

router.include_router(get_league_router)
