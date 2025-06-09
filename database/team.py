from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from scrape.data import GameInfo
from .model import Base
from sqlalchemy.orm import relationship
from sqlalchemy import select

class FootballTeam(Base):
    __tablename__ = "football_teams"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(100), default=False)
    country = Column(String(100), default=False)
    games_as_home = relationship(
        "FootballGame",
        back_populates="home_team",
        foreign_keys="[FootballGame.home_team_id]",
        cascade="all, delete-orphan"
    )

    games_as_away = relationship(
        "FootballGame",
        back_populates="away_team",
        foreign_keys="[FootballGame.away_team_id]",
        cascade="all, delete-orphan"
    )


async def add_team(session: AsyncSession, team_info:dict):
    new_team = FootballTeam(
        name=team_info['name'],
        country=team_info['country'],
    )

    session.add(new_team)
    await session.flush()
    print("partially saved")
    return new_team


async def get_team_by_name(session: AsyncSession, name: str, country: str) -> FootballTeam | None:
    stmt = select(FootballTeam).where(
        FootballTeam.name.ilike(name.strip()),
        FootballTeam.country.ilike(country.strip())
    )
    result = await session.execute(stmt)
    return result.scalars().first()