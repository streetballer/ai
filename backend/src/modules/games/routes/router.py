from fastapi import APIRouter
from src.modules.games.controllers.search_games import router as search_games_router
from src.modules.games.controllers.create_game import router as create_game_router
from src.modules.games.controllers.join_game import router as join_game_router

router = APIRouter()

router.include_router(search_games_router)
router.include_router(create_game_router)
router.include_router(join_game_router)
