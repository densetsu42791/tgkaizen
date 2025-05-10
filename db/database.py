import configparser
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine



config = configparser.ConfigParser()
config.read("config.ini")

DB_URL_psycopg = config["database"]["url_psycopg"]
DB_URL_asyncpg = config["database"]["url_asyncpg"]



sync_engine = create_engine(url=DB_URL_psycopg, echo=True)
async_engine = create_async_engine(url=DB_URL_asyncpg, echo=True)


session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass

# async def main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# if __name__ == "__main__":
#     asyncio.run(main())
