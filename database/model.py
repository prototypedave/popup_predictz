import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from .base import Base, ADMIN_URL, DB_NAME, ASYNC_DATABASE_URL
from .game import FootballGame
from .stats import Stats
from .team import FootballTeam


# Step 1: Ensure database exists
async def ensure_database():
    conn = await asyncpg.connect(ADMIN_URL)
    db_exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", DB_NAME)
    if not db_exists:
        print(f"Creating database: {DB_NAME}")
        await conn.execute(f'CREATE DATABASE "{DB_NAME}"')
    else:
        print(f"Database {DB_NAME} already exists.")
    await conn.close()

# Step 2: Create tables if not present
async def init_tables():
    engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

# Step 3: Main
async def setup_database():
    await ensure_database()
    await init_tables()
