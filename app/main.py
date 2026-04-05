# from scripts.update_dataset import update_dataset

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Football Player Dashboard", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    players = pd.read_csv(DATA_DIR / "players.csv")
    appearances = pd.read_csv(DATA_DIR / "appearances.csv")
    valuations = pd.read_csv(DATA_DIR / "player_valuations.csv")
    games = pd.read_csv(DATA_DIR / "games.csv")
    clubs = pd.read_csv(DATA_DIR / "clubs.csv")

    if "date" in valuations.columns:
        valuations["date"] = pd.to_datetime(valuations["date"], errors="coerce")

    if "date" in games.columns:
        games["date"] = pd.to_datetime(games["date"], errors="coerce")

    return players, appearances, valuations, games, clubs


def find_name_column(df: pd.DataFrame) -> str:
    candidates = ["name", "player_name", "full_name"]
    for col in candidates:
        if col in df.columns:
            return col
    raise ValueError("No encontré una columna de nombre en players.csv")


def build_club_lookup(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = {"club_id", "name"}
    if not required_columns.issubset(df.columns):
        return pd.DataFrame(columns=["club_id", "name"])

    return df[["club_id", "name"]].dropna().drop_duplicates()


st.title("⚽ Football Player Dashboard")

if not DATA_DIR.exists():
    st.error("No se encontró la carpeta data/")
    st.stop()

players, appearances, valuations, games, clubs = load_data()

player_name_col = find_name_column(players)
club_lookup = build_club_lookup(clubs)

player_options = (
    players[["player_id", player_name_col]]
    .dropna()
    .drop_duplicates()
    .sort_values(player_name_col)
)

selected_name = st.selectbox("Seleccioná un jugador", player_options[player_name_col].tolist())

selected_player = player_options[player_options[player_name_col] == selected_name].iloc[0]
player_id = selected_player["player_id"]

player_apps = appearances[appearances["player_id"] == player_id].copy()
player_vals = valuations[valuations["player_id"] == player_id].copy()

if player_apps.empty:
    st.warning("No hay apariciones para este jugador.")
    st.stop()

# Métricas
total_matches = len(player_apps)
minutes = int(player_apps["minutes_played"].fillna(0).sum()) if "minutes_played" in player_apps.columns else 0
goals = int(player_apps["goals"].fillna(0).sum()) if "goals" in player_apps.columns else 0
assists = int(player_apps["assists"].fillna(0).sum()) if "assists" in player_apps.columns else 0
yellow_cards = int(player_apps["yellow_cards"].fillna(0).sum()) if "yellow_cards" in player_apps.columns else 0
red_cards = int(player_apps["red_cards"].fillna(0).sum()) if "red_cards" in player_apps.columns else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Partidos", total_matches)
c2.metric("Minutos", minutes)
c3.metric("Goles", goals)
c4.metric("Asistencias", assists)
c5.metric("Amarillas", yellow_cards)
c6.metric("Rojas", red_cards)

left, right = st.columns(2)

with left:
    st.subheader("Distribución de aportes")
    labels = ["Goles", "Asistencias", "Amarillas", "Rojas"]
    values = [goals, assists, yellow_cards, red_cards]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_ylabel("Cantidad")
    ax.set_title(f"Resumen estadístico de {selected_name}")
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Valor de mercado")
    if not player_vals.empty and "market_value_in_eur" in player_vals.columns and "date" in player_vals.columns:
        vals = player_vals.dropna(subset=["date"]).sort_values("date")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(vals["date"], vals["market_value_in_eur"], marker="o")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Valor en EUR")
        ax.set_title(f"Evolución del valor de mercado de {selected_name}")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No hay datos de valuación disponibles para este jugador.")

st.subheader("Últimos partidos")

if "game_id" in player_apps.columns and "game_id" in games.columns:
    merged = player_apps.merge(games, on="game_id", how="left")

    # Usar directamente las columnas home_club_name y away_club_name de games
    if "home_club_name" in merged.columns and "away_club_name" in merged.columns:
        merged["partido"] = merged["home_club_name"].fillna("") + " vs " + merged["away_club_name"].fillna("")

        cols_to_show = [col for col in [
            "date_y", "competition_id_y", "partido", "minutes_played", "goals", "assists"
        ] if col in merged.columns]
    else:
        cols_to_show = [col for col in [
            "date_y", "competition_id_y", "home_club_id", "away_club_id", "minutes_played", "goals", "assists"
        ] if col in merged.columns]

    if "date_y" in merged.columns:
        merged = merged.sort_values("date_y", ascending=False)

    display_df = merged[cols_to_show].head(10).rename(
        columns={
            "date_y": "Fecha",
            "competition_id_y": "Competición",
            "partido": "Partido",
            "home_club_id": "Equipo local",
            "away_club_id": "Equipo visitante",
            "minutes_played": "Minutos",
            "goals": "Goles",
            "assists": "Asistencias",
        }
    )

    st.dataframe(display_df, use_container_width=True)
else:
    st.info("No se pudieron unir appearances con games por game_id.")

# update_dataset()
