from typing import Any
from src.common.models.response import ResponseModel


def respond(message: str = "", data: dict[str, Any] | None = None) -> ResponseModel:
    return ResponseModel(message=message, data=data or {})
