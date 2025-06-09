import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import aliased
from dataclasses import fields
from .team import FootballTeam
from .game import FootballGame
from .stats import Stats
from scrape.data import MatchStats 
from sqlalchemy import inspect

async def get_all_game_stats_df(session):
    HomeTeam = aliased(FootballTeam)
    AwayTeam = aliased(FootballTeam)

    valid_column_names = Stats.__table__.columns.keys()
    stats_fields = [getattr(Stats, f.name) for f in fields(MatchStats) if f.name in valid_column_names]

    # Add game and team fields
    base_fields = [
        FootballGame.id.label("game_id"),
        FootballGame.date,
        FootballGame.league,
        FootballGame.country,
        FootballGame.round,
        FootballGame.referee,
        FootballGame.venue,
        FootballGame.capacity,
        HomeTeam.name.label("home_team"),
        AwayTeam.name.label("away_team"),
        FootballGame.home_score,
        FootballGame.away_score,
    ]

    stmt = (
        select(*base_fields, *stats_fields)
        .join(Stats, FootballGame.id == Stats.game_id)
        .join(HomeTeam, FootballGame.home_team_id == HomeTeam.id)
        .join(AwayTeam, FootballGame.away_team_id == AwayTeam.id)
    )

    result = await session.execute(stmt)
    df = pd.DataFrame(result.fetchall())
    return df
