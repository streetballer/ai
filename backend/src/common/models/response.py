from pydantic import BaseModel, Field
from typing import Any


class ResponseModel(BaseModel):
    message: str = ""
    data: dict[str, Any] = Field(default_factory=dict)
