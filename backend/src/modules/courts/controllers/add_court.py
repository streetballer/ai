from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.courts.logic.add_court_logic import add_court
from src.modules.courts.models.add_court import AddCourtBody

router = APIRouter()


@router.post("/courts", response_model=ResponseModel)
def add_court_route(
    body: AddCourtBody,
    _: str = Depends(get_current_player_id),
) -> ResponseModel:
    court = add_court(body.lon, body.lat, body.name)
    if court is None:
        raise HTTPException(status_code=409, detail="A court already exists at this location")
    return respond(data={"court": court})
