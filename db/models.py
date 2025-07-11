from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Boolean, UniqueConstraint, text
from db.session import Base
from datetime import datetime


# class Base(DeclarativeBase):
#     pass


class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    join_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    channels: Mapped[list["Channel"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Channel(Base):
    __tablename__ = "channels"

    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    start_count_subs: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"))
    
    subscribers: Mapped[list["Subscriber"]] = relationship(back_populates="channel", cascade="all, delete-orphan")
    user: Mapped["User"] = relationship(back_populates="channels")


class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    invite_link: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    join_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    channel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("channels.channel_id", ondelete="CASCADE"))

    channel: Mapped["Channel"] = relationship(back_populates="subscribers")

    __table_args__ = (UniqueConstraint('user_id', 'channel_id', name='unique_subscriber_per_channel'),)

