from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "player-scores"

def load_data():
    players = pd.read_csv(DATA_DIR / "players.csv")
    scores = pd.read_csv(DATA_DIR / "games.csv")
    return players, scores

import pandas as pd

def get_games_by_team(team_name: str):
    _, games = load_data()

    filtered = games[
        (games["home_club_name"].fillna("").str.lower() == team_name.lower()) |
        (games["away_club_name"].fillna("").str.lower() == team_name.lower())
    ][[
        "game_id",
        "date",
        "home_club_name",
        "away_club_name",
        "home_club_goals",
        "away_club_goals",
        "competition_type"
    ]].copy()

    filtered = filtered.where(pd.notnull(filtered), None)

    return filtered.to_dict(orient="records")