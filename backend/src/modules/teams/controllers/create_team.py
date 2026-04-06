from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.teams.logic.create_team_logic import create_team
from src.modules.teams.models.create_team import CreateTeamBody

router = APIRouter()


@router.post("/teams", response_model=ResponseModel)
def create_team_route(
    body: CreateTeamBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    error, team = create_team(player_id, body.player_id)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Player not found")
    if error in ("already_in_team", "target_in_team"):
        raise HTTPException(status_code=409, detail="Player is already in an active team")
    return respond(data={"team": team})
