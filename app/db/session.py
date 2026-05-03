from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from fastapi import Depends
from app.core.config import settings
from app.db.uow import UnitOfWork

class Database:
    def __init__(self, url: str | None = None):

        self.url = url or self._build_postgres_url()

        self.engine = create_async_engine(
            self.url,
            echo=settings.APP_DEBUG,
            future=True,
            pool_pre_ping=True
        )

        self.SessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            future=True
        )

    def _build_postgres_url(self) -> str:
        return settings.db_url

db=Database()
engine = db.engine
SessionLocal = db.SessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_uow(session: AsyncSession = Depends(get_db)) -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(session) as uow:
        yield uow