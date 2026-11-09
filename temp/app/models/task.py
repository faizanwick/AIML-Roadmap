from datetime import date
from sqlalchemy import Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title : Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description : Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    priority : Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="medium"
    )

    status : Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending"
    )

    due_date : Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    user_id : Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )

    owner : Mapped["User"] = relationship(
        back_populates="tasks"
    )