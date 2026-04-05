from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.auth.logic.sign_up_logic import create_player
from src.modules.auth.logic.verification_logic import send_verification_email
from src.modules.auth.models.sign_up import SignUpBody

router = APIRouter()


@router.post("/auth/sign-up", response_model=ResponseModel)
def sign_up(body: SignUpBody) -> ResponseModel:
    error, result = create_player(body.username, body.email, body.password)
    if error == "username_taken":
        raise HTTPException(status_code=409, detail="Username already taken")
    if error == "email_taken":
        raise HTTPException(status_code=409, detail="Email already taken")
    send_verification_email(result["player_id"], body.email, body.username)
    return respond(data={"access_token": result["access_token"], "refresh_token": result["refresh_token"]})
