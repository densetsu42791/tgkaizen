from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Boolean, UniqueConstraint, text
from sqlalchemy import Enum as SQLAEnum
from enum import Enum
from db.async_session import Base
from datetime import datetime


# class Base(DeclarativeBase):
#     pass


class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    join_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_vizit: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    invite_link: Mapped[str | None] = mapped_column(String(255), nullable=True)

    channels: Mapped[list["Channel"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Channel(Base):
    __tablename__ = "channels"

    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    type_chat: Mapped[str] = mapped_column(String(100), nullable=True)
    invite_link: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_count_subs: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    join_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    disable_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"))
    
    user: Mapped["User"] = relationship(back_populates="channels")
    subscribers: Mapped[list["Subscriber"]] = relationship(back_populates="channel", cascade="all, delete-orphan")
    daily_metrics = relationship("DailyMetric", back_populates="channel")
    

class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    invite_link: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_bot: Mapped[bool] = mapped_column(Boolean)
    is_self: Mapped[bool] = mapped_column(Boolean)
    is_contact: Mapped[bool] = mapped_column(Boolean)
    is_mutual_contact : Mapped[bool] = mapped_column(Boolean)
    is_deleted: Mapped[bool] = mapped_column(Boolean)
    is_verified: Mapped[bool] = mapped_column(Boolean)
    is_restricted: Mapped[bool] = mapped_column(Boolean)
    is_scam: Mapped[bool] = mapped_column(Boolean)
    is_fake: Mapped[bool] = mapped_column(Boolean)
    is_support: Mapped[bool] = mapped_column(Boolean)
    is_premium: Mapped[bool] = mapped_column(Boolean)
    status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_online_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_offline_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    code_language: Mapped[str | None] = mapped_column(String(255), nullable=True)
    emoji_status: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dc_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    photo_small_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    photo_small_id_unique: Mapped[str | None] = mapped_column(String(255), nullable=True)
    restrictions: Mapped[str | None] = mapped_column(String(255), nullable=True)
    join_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    channel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("channels.channel_id", ondelete="CASCADE"))

    channel: Mapped["Channel"] = relationship(back_populates="subscribers")
    activities: Mapped[list["Activity"]] = relationship(back_populates="subscriber", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('user_id', 'channel_id', name='unique_subscriber_per_channel'),)


class ActivityType(Enum):
    SUBSCRIBED = 'join' 
    UNSUBSCRIBED = 'left'


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    activity: Mapped[ActivityType] = mapped_column(SQLAEnum(ActivityType))

    subscriber_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("subscribers.id", ondelete="CASCADE"))
    
    subscriber: Mapped["Subscriber"] = relationship(back_populates="activities")


class DailyMetric(Base):
    __tablename__ = 'daily_metrics'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    subs_total: Mapped[int] = mapped_column(BigInteger)
    subs_today: Mapped[int] = mapped_column(BigInteger)
    unsubs_today: Mapped[int] = mapped_column(BigInteger)

    channel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("channels.channel_id", ondelete="CASCADE"))

    channel = relationship("Channel", back_populates="daily_metrics")