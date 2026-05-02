from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from collections.abc import Generator

from app.core.config import settings

class Database:
    def __init__(self, url: str | None = None):

        self.url = url or self._build_postgres_url()

        self.engine = create_engine(
            self.url,
            echo=settings.APP_DEBUG,
            future=True,
            pool_pre_ping=True
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=Session,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            future=True
        )

    def _build_postgres_url(self) -> str:
        return settings.get_db_url()

    def get_session(self) -> Session:
        return self.SessionLocal()

db=Database()
engine = db.engine
SessionLocal = db.SessionLocal

def get_db() -> Generator[Session, None]:
    with SessionLocal() as session:
        yield session
