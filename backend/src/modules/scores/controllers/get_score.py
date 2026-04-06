from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.scores.logic.get_score_logic import get_score

router = APIRouter()


@router.get("/scores/{score_id}", response_model=ResponseModel)
def get_score_route(score_id: str) -> ResponseModel:
    result = get_score(score_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return respond(data=result)
