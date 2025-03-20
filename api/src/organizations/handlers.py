import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from organizations.logic import get_all_children, verify_key
from organizations.querys import (
    select_cards,
    select_model_by_id,
    select_organization_by_build_id,
    search_org_to_name,
)

from dependencies import add_secret_to_header, get_session, Pagination
from organizations.schemas import RadiusSearchSchema
from crud import (
    get_models,
    get_model,
    create_tables,
    search_org_to_radius,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/building_id={building_id}/organizations",
    summary="Все организации в конкретном здании",
)
async def cards_get(
    secret: Annotated[str, Depends(add_secret_to_header)],
    building_id: Annotated[int, Path()],
    pg: Annotated[Pagination, Depends(Pagination)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """Роутер выводит все организации в здании"""
    verify_key(secret)
    count, q = select_organization_by_build_id(build_id=building_id)

    return await get_models(db=db, pg=pg, count=count, q=q)


@router.get(
    "/activity_id={activity_id}/organizations",
    summary="Все организации с определённым видом деятельности",
    # response_model=GameOneSchema,
)
async def cards_get_to_activity(
    secret: Annotated[str, Depends(add_secret_to_header)],
    activity_id: Annotated[int, Path()],
    db: Annotated[AsyncSession, Depends(get_session)],
    pg: Annotated[Pagination, Depends(Pagination)],
):
    """Роутер выводит все организации в зданииd"""
    verify_key(secret)
    count, q = select_cards()
    cards = await get_models(db=db, pg=pg, count=count, q=q)

    organizations = []

    for card in cards["cards"]:
        for activity in card.activity:
            if activity.id == activity_id:
                organizations.append(card)

    return organizations


@router.get(
    "/organization_id={organization_id}",
    summary="Выводит организацию по её id",
    # response_model=CardResponse,
)
async def get_card(
    secret: Annotated[str, Depends(add_secret_to_header)],
    organization_id: Annotated[int, Path()],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """Роутер выводит карточку с организацией"""
    verify_key(secret)

    q = select_model_by_id(id=organization_id)
    return await get_model(db=db, q=q)


@router.get(
    "/filter/",
    summary="Фильтр организаций по виду дейтельности",
)
async def filter_organization(
    secret: Annotated[str, Depends(add_secret_to_header)],
    db: Annotated[AsyncSession, Depends(get_session)],
    pg: Annotated[Pagination, Depends(Pagination)],
    filter: str | None = Query(None),
):
    """Роутер фильтрует организаций по виду дейтельности"""
    verify_key(secret)

    count, q = select_cards()
    cards = await get_models(db=db, pg=pg, count=count, q=q)

    organizations = []

    for card in cards["cards"]:
        all_cild = []
        for activity in card.activity:
            print(activity.title)
            children_name = get_all_children(activity)
            all_cild.extend(children_name)
        if filter in all_cild:
            organizations.append(card)

    return organizations


@router.get(
    "/search_organization",
    summary="Поиск организации по названию",
)
async def search_organization(
    secret: Annotated[str, Depends(add_secret_to_header)],
    db: Annotated[AsyncSession, Depends(get_session)],
    name: str | None = Query(None),
):
    """Роутер находит организацию по названию"""
    verify_key(secret)
    q = search_org_to_name(name=name)
    return await get_model(db=db, q=q)


@router.post(
    "/radius_search",
    summary="Поиск организации по заданному радиусу",
    # response_model=RadiusSearchSchema,
)
async def radius_search(
    secret: Annotated[str, Depends(add_secret_to_header)],
    db: Annotated[AsyncSession, Depends(get_session)],
    pg: Annotated[Pagination, Depends(Pagination)],
    radius: Annotated[RadiusSearchSchema, Depends()],
):
    """Роутер находит организации в заданном радиусе"""
    verify_key(secret)
    count, q = select_cards()
    cards = await get_models(db=db, pg=pg, count=count, q=q)
    organizations = search_org_to_radius(radius=radius, organizations=cards["cards"])
    return organizations


@router.post(
    "/fill-the-database/",
    summary="Заполнить базу",
    status_code=status.HTTP_201_CREATED,
)
async def fill_the_database(
    secret: Annotated[str, Depends(add_secret_to_header)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> Response:
    """Роутер заполняет базу данных тестовыми данными"""
    verify_key(secret)
    q = select_model_by_id(id=1)
    card = await get_model(db=db, q=q, create=True)
    if card:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="База уже заполнена"
        )
    else:
        await create_tables(db)
        return HTTPException(
            status_code=status.HTTP_201_CREATED, detail="База успешно заполнена"
        )
