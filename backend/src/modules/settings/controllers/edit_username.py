from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.settings.logic.edit_username_logic import edit_username
from src.modules.settings.models.edit_username import EditUsernameBody

router = APIRouter()


@router.post("/settings/username", response_model=ResponseModel)
def edit_username_route(
    body: EditUsernameBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    error = edit_username(player_id, body.username)
    if error == "username_taken":
        raise HTTPException(status_code=409, detail="Username already taken")
    return respond()
