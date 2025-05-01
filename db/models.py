from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, DateTime
from datetime import datetime

# Base = declarative_base()
class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(100))
    first_name: Mapped[str | None] = mapped_column(String(100))
    join_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_vizit: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    channel: Mapped[str | None] = mapped_column(String(255))