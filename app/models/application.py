from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.company import Company

from sqlalchemy import String, Date, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Application(Base):
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        )
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable = False)
    company: Mapped["Company"] = relationship(
        back_populates="applications"
    )
    role: Mapped[str] = mapped_column(
        String(30),
        nullable = False
        )
    status: Mapped[str] = mapped_column(
        Enum(
            "interested",
            "applied",
            "interview",
            "offer",
            "rejected",
            "withdrawn",
            name = "application_status"
        ),
        nullable = False,
        index = True
    )
    job_url: Mapped[str | None] = mapped_column(
        String,
        nullable = True
    )
    deadline: Mapped[date | None] = mapped_column(
        Date,
        nullable = True
    )
    notes: Mapped[str | None] = mapped_column(
        String(150),
        nullable = True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable = False,
        default = datetime.now
    )
    applied_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable = True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable = False,
        default = datetime.now,
        onupdate = datetime.now
    )
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
