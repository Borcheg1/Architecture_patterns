# stdlib
from collections.abc import AsyncGenerator

# thirdparty
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

# fastapi
from fastapi import FastAPI, Request

# project
from src.core.config import settings


def setup_db(app: FastAPI) -> None:
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(settings.database_path), echo=settings.echo_queries, future=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    session_factory = request.app.state.db_session_factory
    async with session_factory() as session:
        yield session
