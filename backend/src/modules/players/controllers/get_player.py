from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.players.logic.get_player_logic import get_player_by_id

router = APIRouter()


@router.get("/players/{player_id}", response_model=ResponseModel)
def get_player(player_id: str) -> ResponseModel:
    player = get_player_by_id(player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return respond(data={"player": player})
