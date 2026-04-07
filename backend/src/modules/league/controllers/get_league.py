from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.league.logic.get_league_logic import get_league

router = APIRouter()


@router.get("/league", response_model=ResponseModel)
def get_league_route(
    place_id: str | None = None,
    court_id: str | None = None,
    team_size: int | None = None,
) -> ResponseModel:
    if not place_id and not court_id:
        raise HTTPException(status_code=422, detail="place_id or court_id is required")
    if team_size is None or team_size < 1:
        raise HTTPException(status_code=422, detail="team_size must be a positive integer")
    standings = get_league(court_id, place_id, team_size)
    if standings is None:
        raise HTTPException(status_code=404, detail="Place or court not found")
    return respond(data={"standings": standings})
