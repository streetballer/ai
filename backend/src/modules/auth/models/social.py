from pydantic import BaseModel


class SocialBody(BaseModel):
    token: str
