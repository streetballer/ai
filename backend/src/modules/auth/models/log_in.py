from pydantic import BaseModel, model_validator


class LogInBody(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str

    @model_validator(mode="after")
    def validate_identifier(self) -> "LogInBody":
        if not self.username and not self.email:
            raise ValueError("Either username or email is required")
        return self
