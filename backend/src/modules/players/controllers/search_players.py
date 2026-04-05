from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.players.logic.search_players_logic import search_players_by_location, search_players_by_text

router = APIRouter()


@router.get("/players", response_model=ResponseModel)
def search_players(
    lon: float | None = None,
    lat: float | None = None,
    text: str | None = None,
) -> ResponseModel:
    has_location = lon is not None and lat is not None
    has_text = text is not None and text.strip() != ""

    if not has_location and not has_text:
        raise HTTPException(status_code=422, detail="Either lon/lat or text is required")
    if (lon is None) != (lat is None):
        raise HTTPException(status_code=422, detail="Both lon and lat are required together")

    if has_location and not has_text:
        players = search_players_by_location(lon, lat)
    else:
        players = search_players_by_text(text, lon if has_location else None, lat if has_location else None)

    return respond(data={"players": players})
