from app.db.session import async_engine
from app.db.models import User, Channel, Base
import asyncio



async def main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())