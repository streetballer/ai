from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.games.logic.create_game_logic import create_or_join_game
from src.modules.games.models.create_game import CreateGameBody

router = APIRouter()


@router.post("/games", response_model=ResponseModel)
def create_game(
    body: CreateGameBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    success = create_or_join_game(body.court_id, body.timestamp, player_id)
    if not success:
        raise HTTPException(status_code=422, detail="Court not found")
    return respond()
