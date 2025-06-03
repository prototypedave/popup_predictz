from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from scrape.data import GameInfo
from .model import Base
from sqlalchemy.orm import relationship


class FootballGame(Base):
    __tablename__ = "football_games"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    league = Column(String(100), nullable=False)
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    round = Column(String(50), nullable=False)
    country = Column(String(100), nullable=False)
    referee = Column(String(100))
    venue = Column(String(100))
    capacity = Column(Integer)

    stats = relationship("Stats", back_populates="game", uselist=False, cascade="all, delete-orphan")


async def add_game(session: AsyncSession, gameinfo: GameInfo):
    new_game = FootballGame(
        date=gameinfo.start_time,
        league=gameinfo.league,
        home_team=gameinfo.home_team,
        away_team=gameinfo.away_team,
        home_score=gameinfo.home_score,
        away_score=gameinfo.away_score,
        round=gameinfo.round,
        country=gameinfo.country,
        referee=gameinfo.referee,
        venue=gameinfo.venue,
        capacity=gameinfo.capacity,
    )
    session.add(new_game)
    await session.flush()
    return new_game