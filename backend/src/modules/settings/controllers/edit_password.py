from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.settings.logic.edit_password_logic import edit_password
from src.modules.settings.models.edit_password import EditPasswordBody

router = APIRouter()


@router.post("/settings/password", response_model=ResponseModel)
def edit_password_route(
    body: EditPasswordBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    error = edit_password(player_id, body.old_password, body.new_password)
    if error == "wrong_password":
        raise HTTPException(status_code=422, detail="Old password is incorrect")
    return respond()
