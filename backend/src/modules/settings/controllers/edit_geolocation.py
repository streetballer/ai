from fastapi import APIRouter, Depends
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.settings.logic.edit_geolocation_logic import edit_geolocation
from src.modules.settings.models.edit_geolocation import EditGeolocationBody

router = APIRouter()


@router.post("/settings/geolocation", response_model=ResponseModel)
def edit_geolocation_route(
    body: EditGeolocationBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    edit_geolocation(player_id, body.lon, body.lat)
    return respond()
