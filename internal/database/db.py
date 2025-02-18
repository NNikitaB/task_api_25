from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase,declarative_base
from sqlalchemy_utils import database_exists, create_database # type: ignore
from sqlalchemy import MetaData
import logging


url = "sqlite+aiosqlite://"
#url = "sqlite+aiosqlite:////T:\\VSC_PROJECTS\\python_servise_api\\app\\db\\file.db"

engine = create_async_engine(url=url)

#if not database_exists(engine.url):
#    create_database(engine.url)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#class Base(DeclarativeBase):
#    abstract = True
#    pass

#Base = declarative_base()

async def get_async_session():
    async with async_session_maker() as session:
        yield session