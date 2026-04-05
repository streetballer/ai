from pydantic import BaseModel


class AddCourtBody(BaseModel):
    lon: float
    lat: float
    name: str
