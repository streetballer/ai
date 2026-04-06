from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.teams.logic.search_teams_logic import search_teams_by_court, search_teams_by_location

router = APIRouter()


@router.get("/teams", response_model=ResponseModel)
def search_teams(
    court_id: str | None = None,
    lon: float | None = None,
    lat: float | None = None,
) -> ResponseModel:
    has_court = court_id is not None
    has_location = lon is not None and lat is not None

    if not has_court and not has_location:
        raise HTTPException(status_code=422, detail="Either court_id or lon/lat is required")
    if not has_court and (lon is None) != (lat is None):
        raise HTTPException(status_code=422, detail="Both lon and lat are required together")

    if has_court:
        teams = search_teams_by_court(court_id)
    else:
        teams = search_teams_by_location(lon, lat)

    return respond(data={"teams": teams})
