from fastapi import APIRouter
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond

router = APIRouter()


@router.get("/health-check", response_model=ResponseModel)
def health_check() -> ResponseModel:
    return respond()
