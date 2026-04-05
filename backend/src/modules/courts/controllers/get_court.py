from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.courts.logic.get_court_logic import get_court_by_id

router = APIRouter()


@router.get("/courts/{court_id}", response_model=ResponseModel)
def get_court(court_id: str) -> ResponseModel:
    court = get_court_by_id(court_id)
    if court is None:
        raise HTTPException(status_code=404, detail="Court not found")
    return respond(data={"court": court})
