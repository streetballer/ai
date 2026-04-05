from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.modules.auth.models.social import SocialBody

router = APIRouter()


@router.post("/auth/google", response_model=ResponseModel)
def google_auth(body: SocialBody) -> ResponseModel:
    raise HTTPException(status_code=498, detail="Token expired or invalid")


@router.post("/auth/apple", response_model=ResponseModel)
def apple_auth(body: SocialBody) -> ResponseModel:
    raise HTTPException(status_code=498, detail="Token expired or invalid")


@router.post("/auth/facebook", response_model=ResponseModel)
def facebook_auth(body: SocialBody) -> ResponseModel:
    raise HTTPException(status_code=498, detail="Token expired or invalid")
