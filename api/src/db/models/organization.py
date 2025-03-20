from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped
from db import Base
from db.models.mixins.dates import CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from api.src.db.models.building import Building
    from api.src.db.models.activity import Activity


class Organization(CreatedAtMixin, UpdatedAtMixin, Base):
    """Модель организации"""

    id: Mapped[int] = Column(
        Integer, primary_key=True, index=True, unique=True, nullable=False
    )

    title: Mapped[String] = Column(String, nullable=False)
    phone: Mapped[list[String]] = Column(ARRAY(String), nullable=False)
    # activity_id: Mapped[int] = Column(
    #     Integer, ForeignKey("activitys.id", ondelete="CASCADE")
    # )

    activity: Mapped[list["Activity"]] = relationship(
        "Activity", secondary="actorgs", back_populates="organizations"
    )
    build_id: Mapped[int] = Column(
        Integer, ForeignKey("buildings.id", ondelete="CASCADE")
    )

    building: Mapped["Building"] = relationship(
        "Building",
        back_populates="organizations",
    )
