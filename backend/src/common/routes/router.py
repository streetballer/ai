from fastapi import APIRouter
from src.common.controllers.health_check import router as health_check_router
from src.modules.auth.routes.router import router as auth_router
from src.modules.players.routes.router import router as players_router
from src.modules.courts.routes.router import router as courts_router
from src.modules.games.routes.router import router as games_router
from src.modules.places.routes.router import router as places_router
from src.modules.teams.routes.router import router as teams_router
from src.modules.scores.routes.router import router as scores_router
from src.modules.league.routes.router import router as league_router
from src.modules.settings.routes.router import router as settings_router

router = APIRouter()

router.include_router(health_check_router)
router.include_router(auth_router)
router.include_router(players_router)
router.include_router(courts_router)
router.include_router(games_router)
router.include_router(places_router)
router.include_router(teams_router)
router.include_router(scores_router)
router.include_router(league_router)
router.include_router(settings_router)
