from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declared_attr
from typing import Any
from settings import settings
from sqlalchemy.orm import as_declarative

from sqlalchemy.orm import class_mapper


@as_declarative()
class BaseModel:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=False)
        self._session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    async def create_database(self) -> None:
        async with self._engine.connect() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)
            await conn.commit()

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        async with self._session_factory() as session:
            yield session


database_instance = Database(settings.DATABASE_URL_asyncpg)
