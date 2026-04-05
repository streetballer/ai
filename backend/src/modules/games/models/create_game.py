from datetime import datetime
from pydantic import BaseModel


class CreateGameBody(BaseModel):
    court_id: str
    timestamp: datetime
