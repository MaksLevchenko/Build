from typing import Annotated

from fastapi import Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from organizations.schemas import RadiusSearchSchema
from db import Base
from dependencies import Pagination, get_session
from querys import add_new_model, delete_model_by_id, update_model_q


async def get_models(
    db: Annotated[AsyncSession, Depends(get_session)],
    pg: Annotated[Pagination, Depends(Pagination)],
    count: str,
    q: Annotated[str, Query(default="*")],
):
    _count = await db.execute(count)
    _exe = await db.execute(q.offset(pg.offset).limit(pg.limit))
    return {
        "pages": {**pg.dict, "count": _count.scalar()},
        "cards": _exe.scalars().all(),
    }


async def get_model(
    db: Annotated[AsyncSession, Depends(get_session)],
    q: Annotated[str, Query(default="*")],
    create: bool = False,
):
    card = await db.execute(q)
    card = card.scalar()
    if card:
        return card
    else:
        if create:
            return False
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="there is no such card"
            )


async def add_model(
    db: Annotated[AsyncSession, Depends(get_session)],
    schema: Annotated[Base, Query(response_model=Base)],
    model: Base,
):
    q = add_new_model(schema=schema, model=model)
    await db.execute(q)
    await db.commit()
    return schema


async def update_model(
    db: Annotated[AsyncSession, Depends(get_session)],
    model: Base,
    schema: Annotated[Base, Query(response_model=Base)],
):
    q = update_model_q(model=model, schema=schema)
    await db.execute(q)
    await db.commit()
    return schema


def search_org_to_radius(radius: RadiusSearchSchema, organizations: list):
    """Поиск организации по заданному радиусу"""

    rad = radius.radius * 0.00001
    latitude_min = radius.latitude - rad
    latitude_max = radius.latitude + rad
    longitude_min = radius.longitude - rad
    longitude_max = radius.longitude + rad
    organizations_list = []
    for i in organizations:
        if (
            latitude_min <= i.building.latitude <= latitude_max
            and longitude_min <= i.building.longitude <= longitude_max
        ):
            organizations_list.append(i)
    return organizations_list
