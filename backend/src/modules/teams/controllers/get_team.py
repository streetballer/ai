from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.teams.logic.get_team_logic import get_team_by_id

router = APIRouter()


@router.get("/teams/{team_id}", response_model=ResponseModel)
def get_team(
    team_id: str,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    result = get_team_by_id(team_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return respond(data=result)
