import asyncio
from db.models import Base
from db.database import engine
from sqlalchemy import text


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())



# Добавить столбец
# with engine.connect() as conn:
#     conn.execute(text("ALTER TABLE users ADD COLUMN age INTEGER"))



# reset_db.py
# from db.database import engine, Base
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# import asyncio
# async def reset_db():
#     # Закрытие всех таблиц и удаление данных
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         print("⚠️ Все таблицы удалены.")
    
#     # Пересоздание таблиц
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#         print("✅ Все таблицы созданы заново.")

# if __name__ == "__main__":
#     asyncio.run(reset_db())