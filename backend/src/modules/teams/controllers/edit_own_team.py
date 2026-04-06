from fastapi import APIRouter, Depends, HTTPException
from src.common.middleware.auth import get_current_player_id
from src.common.models.response import ResponseModel
from src.common.utilities.respond import respond
from src.modules.teams.logic.edit_team_logic import edit_team
from src.modules.teams.models.edit_team import EditTeamBody

router = APIRouter()


@router.post("/teams/team", response_model=ResponseModel)
def edit_own_team(
    body: EditTeamBody,
    player_id: str = Depends(get_current_player_id),
) -> ResponseModel:
    has_color = body.color is not None
    has_add = body.add_player_ids is not None and len(body.add_player_ids) > 0
    has_remove = body.remove_player_ids is not None and len(body.remove_player_ids) > 0

    if not has_color and not has_add and not has_remove:
        raise HTTPException(status_code=422, detail="At least one of color, add_player_ids, or remove_player_ids is required")

    error = edit_team(player_id, body.color, body.add_player_ids, body.remove_player_ids)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Player not found")
    if error == "no_team":
        raise HTTPException(status_code=404, detail="No active team found")
    return respond()
