from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from organizations.querys import select_model_by_id
from db.models.activity import Activity
from db.models.building import Building
from db.models.organization import Organization
from organizations.schemas import ActivitySchema, OrganizationSchema, BuildingSchema
from dependencies import get_session
from .crud import (
    get_models,
    add_model,
    get_model,
    update_model,
    search_org_to_radius,
)


async def create_tables(
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """Создаёт тестовые таблицы в базе"""

    activitys = [
        {"title": "Еда", "level": 0, "parent_id": None},
        {"title": "Молочные продукты", "level": 1, "parent_id": 1},
        {"title": "Мясо", "level": 1, "parent_id": 1},
        {"title": "Говядина", "level": 2, "parent_id": 3},
        {"title": "Транспорт", "level": 0, "parent_id": None},
        {"title": "Легковые автомобили", "level": 1, "parent_id": 5},
    ]

    buildings = [
        {
            "address": "Котельническая наб., 33 1",
            "latitude": 55.7472222,
            "longitude": 37.6427778,
        },
        {"address": "Театральная пл., 1", "longitude": 37.61849, "latitude": 55.75932},
        {
            "address": "Лаврушинский пер., 10",
            "latitude": 55.7340466,
            "longitude": 37.6164066,
        },
        {
            "address": "Андропова пр-т, 1",
            "latitude": 55.6941283,
            "longitude": 37.6694633,
        },
    ]

    organizations = [
        {
            "title": "ООО 'Вкус вилл'",
            "phone": ["+7 (495) 777-77-77", "+7 (495) 777-77-78"],
            "build_id": 1,
        },
        {
            "title": "ООО 'Мерседес'",
            "phone": ["+7 (495) 777-77-77", "+7 (495) 777-77-78"],
            "build_id": 1,
        },
        {
            "title": "ООО 'Весёлый молочник'",
            "phone": ["+7 (495) 777-77-77", "+7 (495) 777-77-78"],
            "build_id": 2,
        },
        {
            "title": "ООО 'Суини Тодд'",
            "phone": ["+7 (495) 777-77-77", "+7 (495) 777-77-78"],
            "build_id": 3,
        },
    ]

    for activity in activitys:
        activity = ActivitySchema(**activity)
        await add_model(db=db, schema=activity, model=Activity)

    for building in buildings:
        building = BuildingSchema(**building)
        await add_model(db=db, schema=building, model=Building)

    await create_org(db=db, id=1, org_index=organizations[0], act_ids=[1, 2, 3, 4])
    await create_org(db=db, id=2, org_index=organizations[1], act_ids=[6])
    await create_org(db=db, id=3, org_index=organizations[2], act_ids=[2])
    await create_org(db=db, id=4, org_index=organizations[3], act_ids=[3, 4])


async def create_org(db, id: int, org_index: dict, act_ids: list[int]):

    organization = OrganizationSchema(**org_index)
    org = await add_model(db=db, schema=organization, model=Organization)
    q = select_model_by_id(id)
    org = await get_model(db=db, q=q)

    for act_id in act_ids:
        q = select()
        q = (
            q.add_columns(Activity)
            .options(selectinload(Activity.organizations))
            .where(Activity.id == act_id)
        )
        act = await get_model(db=db, q=q)
        org.activity.append(act)
        await db.commit()
