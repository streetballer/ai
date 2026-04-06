from pydantic import BaseModel, field_validator, model_validator


class SubmitScoreBody(BaseModel):
    score_1: int
    score_2: int
    opponent_id: str

    @field_validator("score_1", "score_2")
    @classmethod
    def score_in_range(cls, value: int) -> int:
        if value < 0 or value > 99:
            raise ValueError("Score must be between 0 and 99")
        return value

    @model_validator(mode="after")
    def scores_not_tied(self) -> "SubmitScoreBody":
        if self.score_1 == self.score_2:
            raise ValueError("Tied scores are not allowed")
        return self
