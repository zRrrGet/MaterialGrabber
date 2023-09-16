from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
from sqlalchemy import insert

from .models import Base


async def create_pool(
    connection_uri: str = "postgresql+asyncpg://postgres:postgres@localhost/postgres",
):
    engine = create_async_engine(connection_uri)
    if not database_exists(connection_uri):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    pool = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    return pool
