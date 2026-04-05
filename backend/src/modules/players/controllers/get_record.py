from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.players.logic.get_record_logic import get_record_with_player

router = APIRouter()


@router.get("/players/{player_id}/record", response_model=ResponseModel)
def get_record(
    player_id: str,
    current_player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    record = get_record_with_player(current_player_id, player_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return respond(data=record)
