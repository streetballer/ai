from pydantic import BaseModel, EmailStr


class EditEmailBody(BaseModel):
    email: EmailStr
