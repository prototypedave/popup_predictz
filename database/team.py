from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from scrape.data import GameInfo
from .model import Base
from sqlalchemy.orm import relationship

class FootballTeam(Base):
    __tablename__ = "football_teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), default=False)
    country = Column(String(100), default=False)
    venue = Column(String(100), default=False)
    capacity = Column(Integer)
    games = relationship("FootballGame", back_populates="team", uselist=True, cascade="all, delete-orphan")