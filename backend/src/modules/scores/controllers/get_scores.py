from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.scores.logic.get_scores_logic import get_scores

router = APIRouter()


@router.get("/scores", response_model=ResponseModel)
def get_scores_route(
    player_id: str | None = None,
    confirmed: bool | None = None,
    _: str = Depends(get_current_player_id),
) -> ResponseModel:
    if not player_id:
        raise HTTPException(status_code=422, detail="player_id is required")
    scores = get_scores(player_id, confirmed)
    return respond(data={"scores": scores})
