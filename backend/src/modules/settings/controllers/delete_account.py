from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.settings.logic.delete_account_logic import delete_account
from src.modules.settings.models.delete_account import DeleteAccountBody

router = APIRouter()


@router.post("/settings/delete-account", response_model=ResponseModel)
def delete_account_route(
    body: DeleteAccountBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    error = delete_account(player_id, body.password)
    if error == "wrong_password":
        raise HTTPException(status_code=422, detail="Password is incorrect")
    return respond()
