from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.games.logic.join_game_logic import join_game

router = APIRouter()


@router.post("/games/{game_id}/join", response_model=ResponseModel)
def join_game_route(
    game_id: str,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    result = join_game(game_id, player_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Game not found")
    if result == "past":
        raise HTTPException(status_code=403, detail="Game has already started")
    return respond()
