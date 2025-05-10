# from models import User, Channel, Subscriber
# from database import engine, Base
# import asyncio


# async def main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# if __name__ == "__main__":
#     asyncio.run(main())