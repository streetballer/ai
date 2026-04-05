from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.players.logic.get_player_logic import get_own_player

router = APIRouter()


@router.get("/players/player", response_model=ResponseModel)
def get_own_player_route(player_id: str = Depends(get_current_player_id)) -> ResponseModel:
    player = get_own_player(player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return respond(data={"player": player})
