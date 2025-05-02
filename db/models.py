from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Boolean, UniqueConstraint
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(100))
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    join_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_vizit: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    leave_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    channel_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("channels.channel_id", ondelete="SET NULL"),
        unique=True  # один канал на одного юзера
    )

    channel: Mapped["Channel"] = relationship(
        "Channel",
        back_populates="user",
        uselist=False
    )


class Channel(Base):
    __tablename__ = "channels"

    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255))
    type_channel: Mapped[str | None] = mapped_column(String(100))
    is_private_channel: Mapped[bool | None] = mapped_column(Boolean, default=False)
    start_count_subs: Mapped[int | None] = mapped_column(BigInteger)
    join_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="channel",
        uselist=False
    )

