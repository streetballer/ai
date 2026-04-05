from pydantic import BaseModel, model_validator


class PasswordResetRequestBody(BaseModel):
    username: str | None = None
    email: str | None = None

    @model_validator(mode="after")
    def validate_identifier(self) -> "PasswordResetRequestBody":
        if not self.username and not self.email:
            raise ValueError("Either username or email is required")
        return self
