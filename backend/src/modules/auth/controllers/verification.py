from fastapi import APIRouter, HTTPException
from src.common.libraries.jwt import decode_token
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.auth.logic.verification_logic import verify_email

router = APIRouter()


@router.post("/auth/verification/{token}", response_model=ResponseModel)
def verify_email_endpoint(token: str) -> ResponseModel:
    payload = decode_token(token)
    if payload is None or payload.get("type") != "email_verification":
        raise HTTPException(status_code=498, detail="Token expired or invalid")
    verify_email(payload["sub"])
    return respond()
