from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Boolean, UniqueConstraint, text
from app.db.session import Base
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
    
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="channels")

