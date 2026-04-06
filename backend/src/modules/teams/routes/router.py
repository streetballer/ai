from fastapi import APIRouter
from src.modules.teams.controllers.search_teams import router as search_teams_router
from src.modules.teams.controllers.create_team import router as create_team_router
from src.modules.teams.controllers.get_own_team import router as get_own_team_router
from src.modules.teams.controllers.edit_own_team import router as edit_own_team_router
from src.modules.teams.controllers.get_standings import router as get_standings_router
from src.modules.teams.controllers.get_team import router as get_team_router

router = APIRouter()

router.include_router(search_teams_router)
router.include_router(create_team_router)
router.include_router(get_own_team_router)
router.include_router(edit_own_team_router)
router.include_router(get_standings_router)
router.include_router(get_team_router)
