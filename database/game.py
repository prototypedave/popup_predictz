from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from scrape.data import GameInfo
from .model import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, select


class FootballGame(Base):
    __tablename__ = "football_games"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    league = Column(String(100), nullable=False)
    home_team_id = Column(Integer, ForeignKey("football_teams.id"))
    away_team_id = Column(Integer, ForeignKey("football_teams.id"))
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    round = Column(String(50), nullable=True)
    country = Column(String(100), nullable=False)
    referee = Column(String(100))
    venue = Column(String(100))
    capacity = Column(Integer)

    home_team = relationship("FootballTeam", back_populates="games_as_home", foreign_keys=[home_team_id])
    away_team = relationship("FootballTeam", back_populates="games_as_away", foreign_keys=[away_team_id])

    stats = relationship("Stats", back_populates="game", uselist=False, cascade="all, delete-orphan")
    #players = relationship("Players", back_populates="game", uselist=False, cascade="all, delete-orphan")
    

async def add_game(session: AsyncSession, gameinfo: dict):
    new_game = FootballGame(
        date=gameinfo['start_time'],
        league=gameinfo['league'],
        home_team=gameinfo['home_team'],
        away_team=gameinfo['away_team'],
        home_score=gameinfo['home_score'],
        away_score=gameinfo['away_score'],
        round=gameinfo['round'],
        country=gameinfo['country'],
        referee=gameinfo['referee'],
        venue=gameinfo['venue'],
        capacity=gameinfo['capacity'],
    )
    session.add(new_game)
    await session.flush()
    print("partially saved")
    return new_game


async def is_game_already_saved(session: AsyncSession, home: int, away: int) -> FootballGame | None:
    stmt = select(FootballGame).where(
        FootballGame.home_team_id == home,
        FootballGame.away_team_id == away
    )
    result = await session.execute(stmt)
    return result.scalars().first()
