"""
Схемы для моделей
"""

from pydantic import BaseModel


class ActivitySchema(BaseModel):
    """Схема для активностей"""

    title: str
    level: int
    parent_id: int | None


class BuildingCoordinatesSchema(BaseModel):
    """Схема для координат здания"""

    latitude: float
    longitude: float


class RadiusSearchSchema(BuildingCoordinatesSchema):
    """Схема для поиска зданий по заданному радиусу"""

    radius: float


class BuildingSchema(BuildingCoordinatesSchema):
    """Схема для здания"""

    address: str


class OrganizationSchema(BaseModel):
    """Схема для организации"""

    title: str
    phone: list[str]
    build_id: int
