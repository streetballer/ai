from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.scores.logic.submit_score_logic import submit_score
from src.modules.scores.models.submit_score import SubmitScoreBody

router = APIRouter()

_UNPROCESSABLE_ERRORS = {
    "player_not_found",
    "no_active_team",
    "opponent_not_found",
    "opponent_no_active_team",
    "same_team",
}


@router.post("/scores", response_model=ResponseModel)
def submit_score_route(
    body: SubmitScoreBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    error, score = submit_score(player_id, body.score_1, body.score_2, body.opponent_id)
    if error in _UNPROCESSABLE_ERRORS:
        raise HTTPException(status_code=422, detail=error)
    return respond(data={"score": score})
