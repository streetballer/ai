from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.courts.logic.search_courts_logic import search_courts_by_location, DEFAULT_RADIUS_METERS

router = APIRouter()


@router.get("/courts", response_model=ResponseModel)
def search_courts(
    lon: float | None = None,
    lat: float | None = None,
    radius: float = DEFAULT_RADIUS_METERS,
) -> ResponseModel:
    if lon is None or lat is None:
        raise HTTPException(status_code=422, detail="Both lon and lat are required")
    courts = search_courts_by_location(lon, lat, radius)
    return respond(data={"courts": courts})
