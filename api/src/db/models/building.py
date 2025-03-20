import enum
from typing import TYPE_CHECKING
from sqlalchemy import Column, String, DECIMAL, Integer
from sqlalchemy.orm import Mapped, relationship
from db import Base
from db.models.mixins.dates import CreatedAtMixin

if TYPE_CHECKING:
    from api.src.db.models.organization import Organization


class Building(CreatedAtMixin, Base):
    """Модель здания"""

    id: Mapped[int] = Column(
        Integer, primary_key=True, index=True, unique=True, nullable=False
    )

    address: Mapped[String] = Column(String, nullable=False)
    latitude: Mapped[float] = Column(DECIMAL, nullable=False)
    longitude: Mapped[float] = Column(DECIMAL, nullable=False)

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        back_populates="building",
    )
