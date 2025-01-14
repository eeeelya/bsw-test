from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.postgresql.database import db


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_db_session = db.session_maker()

    try:
        yield async_db_session

        await async_db_session.commit()
    except Exception:
        await async_db_session.rollback()
        raise
    finally:
        await async_db_session.close()
