from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.settings.logic.edit_email_logic import edit_email
from src.modules.settings.models.edit_email import EditEmailBody

router = APIRouter()


@router.post("/settings/email", response_model=ResponseModel)
def edit_email_route(
    body: EditEmailBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    error = edit_email(player_id, str(body.email))
    if error == "email_taken":
        raise HTTPException(status_code=409, detail="Email already taken")
    return respond()
