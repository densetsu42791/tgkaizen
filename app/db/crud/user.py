from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User


import logging
logger = logging.getLogger(__name__)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.user_id == user_id)
    logger.info(f"Func get_user.stmt: {stmt}")
    result = await session.execute(stmt)
    logger.info(f"Func get_user.result: {result}")
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user: User):
    logger.info(f"RUN func create_user")
    session.add(user)
    await session.commit()