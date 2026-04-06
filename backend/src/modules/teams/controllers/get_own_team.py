from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.teams.logic.get_own_team_logic import get_own_team

router = APIRouter()


@router.get("/teams/team", response_model=ResponseModel)
def get_own_team_route(player_id: str = Depends(get_current_player_id)) -> ResponseModel:
    result = get_own_team(player_id)
    if result is None:
        raise HTTPException(status_code=404, detail="No active team found")
    return respond(data=result)
