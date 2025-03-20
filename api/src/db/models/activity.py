from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint, Table
from sqlalchemy.orm import Mapped, relationship
from db import Base
from db.models.mixins.dates import CreatedAtMixin

if TYPE_CHECKING:
    from api.src.db.models.organization import Organization


class Activity(CreatedAtMixin, Base):
    """Модель деятельности"""

    id: Mapped[int] = Column(
        Integer, primary_key=True, index=True, unique=True, nullable=False
    )

    title: Mapped[String] = Column(String, nullable=False)

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", secondary="actorgs", back_populates="activity"
    )

    parent_id: Mapped[int | None] = Column(
        Integer, ForeignKey("activitys.id", ondelete="CASCADE"), nullable=True
    )
    level: Mapped[int] = Column(Integer, nullable=False)

    __table_args__ = (CheckConstraint(level <= 3),)

    # Настройка каскадирования операций
    children: Mapped[list["Activity"]] = relationship(
        "Activity",
        remote_side=[id],
        backref="parent",
        lazy="selectin",
        join_depth=3,
    )


association_table = Table(
    "actorgs",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activitys.id"), primary_key=True),
)
# class ActOrg(Base.metadata):
#     """Модель связи между деятельностью и организацией"""

#     __tablename__ = "actorgs"

#     organization_id = Column(Integer, ForeignKey("organizations.id"), primary_key=True)
#     activity_id = Column(Integer, ForeignKey("activitys.id"), primary_key=True)
