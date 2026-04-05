from fastapi import APIRouter, HTTPException
from src.common.libraries.jwt import decode_token
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.auth.logic.token_logic import rotate_tokens

router = APIRouter()


@router.post("/auth/refresh/{token}", response_model=ResponseModel)
def refresh_tokens(token: str) -> ResponseModel:
    payload = decode_token(token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=498, detail="Token expired or invalid")
    result = rotate_tokens(payload["sub"], token)
    if result is None:
        raise HTTPException(status_code=498, detail="Token expired or invalid")
    return respond(data=result)
