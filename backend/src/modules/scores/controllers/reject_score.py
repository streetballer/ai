from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.scores.logic.reject_score_logic import reject_score

router = APIRouter()


@router.post("/scores/{score_id}/reject", response_model=ResponseModel)
def reject_score_route(
    score_id: str,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    result = reject_score(score_id, player_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Score not found")
    if result == "not_in_score":
        raise HTTPException(status_code=403, detail="Player is not part of this score")
    return respond()
