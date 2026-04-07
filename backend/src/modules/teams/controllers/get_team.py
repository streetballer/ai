from typing import Literal
from fastapi import APIRouter, HTTPException
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.teams.logic.get_team_logic import get_team_by_id, get_team_by_player_id

router = APIRouter()


@router.get("/teams/{team_id}", response_model=ResponseModel)
def get_team(team_id: str, by: Literal["team", "player"] | None = None) -> ResponseModel:
    if by == "player":
        result = get_team_by_player_id(team_id)
    elif by == "team":
        result = get_team_by_id(team_id)
    else:
        result = get_team_by_id(team_id) or get_team_by_player_id(team_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return respond(data=result)
