from pydantic import BaseModel


class CreateTeamBody(BaseModel):
    player_id: str
