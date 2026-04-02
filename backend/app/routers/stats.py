from fastapi import APIRouter
from app.services.data_service import get_games_by_team

router = APIRouter()

@router.get("/team/{team_name}/games")
def team_games(team_name: str):
    return get_games_by_team(team_name)