from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.places.logic.search_places_logic import search_places

router = APIRouter()


@router.get("/places", response_model=ResponseModel)
def search_places_route(
    text: str | None = None,
    lon: float | None = None,
    lat: float | None = None,
) -> ResponseModel:
    has_text = text is not None and text.strip() != ""
    has_location = lon is not None and lat is not None

    if not has_text and not has_location:
        raise HTTPException(status_code=422, detail="Either text or lon/lat is required")
    if (lon is None) != (lat is None):
        raise HTTPException(status_code=422, detail="Both lon and lat are required together")

    places = search_places(text if has_text else None, lon, lat)
    return respond(data={"places": places})
