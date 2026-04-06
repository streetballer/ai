from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.auth.logic.log_in_logic import authenticate_player
from src.modules.auth.models.log_in import LogInBody

router = APIRouter()


@router.post("/auth/log-in", response_model=ResponseModel)
def log_in(body: LogInBody) -> ResponseModel:
    result = authenticate_player(body.password, body.username, body.email)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return respond(data={"access_token": result.access_token, "refresh_token": result.refresh_token})
