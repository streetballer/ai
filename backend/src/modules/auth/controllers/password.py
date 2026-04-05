from fastapi import APIRouter, HTTPException
from src.common.libraries.jwt import decode_token
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.auth.logic.password_logic import request_password_reset, reset_password
from src.modules.auth.models.password_reset import PasswordResetBody
from src.modules.auth.models.password_reset_request import PasswordResetRequestBody

router = APIRouter()


@router.post("/auth/password", response_model=ResponseModel)
def request_reset(body: PasswordResetRequestBody) -> ResponseModel:
    request_password_reset(body.username, body.email)
    return respond()


@router.post("/auth/password/{token}", response_model=ResponseModel)
def do_reset(token: str, body: PasswordResetBody) -> ResponseModel:
    payload = decode_token(token)
    if payload is None or payload.get("type") != "password_reset":
        raise HTTPException(status_code=498, detail="Token expired or invalid")
    reset_password(payload["sub"], body.password)
    return respond()
