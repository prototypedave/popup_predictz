from sqlalchemy import Column, Integer, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from scrape.data import PlayerStats
from .model import Base
from dataclasses import asdict
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Players(Base):
    __tablename__ = "match_stats"

    game_id = Column(Integer, ForeignKey("football_games.id", ondelete="CASCADE"), unique=True, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    general = Column(JSON, nullable=False)
    goal_keeping = Column(JSON, nullable=False)
    defensive = Column(JSON, nullable=False)
    attacking = Column(JSON, nullable=False)
    passing = Column(JSON, nullable=False)
    shots = Column(JSON, nullable=False)

    game = relationship("FootballGame", back_populates="players")
    

async def add_players(session: AsyncSession, player: PlayerStats, game_id: int):
    new_players = Players(
        general=player.general,
        goal_keeping=player.goalkeeping,
        defensive=player.defensive,
        attacking=player.attacking,
        passing=player.passing,
        shots=player.shots
    )
    session.add(new_players)
    await session.commit()
    print("Players saved for game ID:", game_id)