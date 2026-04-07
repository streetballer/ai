from pydantic import BaseModel


class DeleteAccountBody(BaseModel):
    password: str
