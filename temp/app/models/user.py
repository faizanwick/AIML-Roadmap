from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name : Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email : Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    hashed_password : Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    tasks : Mapped[list["Task"]] = relationship(
        back_populates="owner"
    )