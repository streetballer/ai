import re
from pydantic import BaseModel, field_validator


class EditTeamBody(BaseModel):
    color: str | None = None
    add_player_ids: list[str] | None = None
    remove_player_ids: list[str] | None = None

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: str | None) -> str | None:
        if value is not None and not re.match(r"^#[0-9A-Fa-f]{6}$", value):
            raise ValueError("color must be a hex color code like #20DFBF")
        return value
