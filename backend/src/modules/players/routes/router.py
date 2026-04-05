from fastapi import APIRouter
from src.modules.players.controllers.search_players import router as search_players_router
from src.modules.players.controllers.get_own_player import router as get_own_player_router
from src.modules.players.controllers.get_record import router as get_record_router
from src.modules.players.controllers.get_player import router as get_player_router

router = APIRouter()

# get_own_player and get_record must be registered before get_player to avoid path conflicts
router.include_router(search_players_router)
router.include_router(get_own_player_router)
router.include_router(get_record_router)
router.include_router(get_player_router)
