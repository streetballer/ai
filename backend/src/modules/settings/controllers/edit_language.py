from fastapi import APIRouter, Depends
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.settings.logic.edit_language_logic import edit_language
from src.modules.settings.models.edit_language import EditLanguageBody

router = APIRouter()


@router.post("/settings/language", response_model=ResponseModel)
def edit_language_route(
    body: EditLanguageBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    edit_language(player_id, body.language)
    return respond()
