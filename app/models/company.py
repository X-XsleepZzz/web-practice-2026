from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.application import Base

if TYPE_CHECKING:
    from app.models.application import Application

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    website: Mapped[str | None] = mapped_column(String, nullable=True)
    applications: Mapped[list["Application"]] = relationship(
        back_populates="company",
        cascade="all, delete",
        passive_deletes=True,
    )
