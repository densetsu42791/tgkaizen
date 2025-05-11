from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import configparser


config = configparser.ConfigParser()
config.read("config.ini")


DB_URL=config["database"]["url_asyncpg"]
 

async_engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass