from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from db.models import Organization


def select_cards():

    q = select()

    count = q.add_columns(func.count(Organization.id).label("count"))
    q = (
        q.add_columns(Organization)
        .options(selectinload(Organization.activity))
        .options(selectinload(Organization.building))
    )
    q = q.order_by(Organization.title)
    return count, q


def select_model_by_id(id: int):

    q = select()
    q = (
        q.add_columns(Organization)
        .options(selectinload(Organization.activity))
        .options(selectinload(Organization.building))
        .where(Organization.id == id)
    )
    return q


def select_organization_by_build_id(build_id: int):

    q = select()
    count = (
        q.add_columns(func.count())
        .select_from(Organization)
        .filter(Organization.build_id == build_id)
    )
    q = (
        q.add_columns(Organization)
        .options(selectinload(Organization.activity))
        .where(Organization.build_id == build_id)
    )
    return count, q


def search_org_to_name(name: str):
    """Поиск по названию"""
    q = select()
    q = (
        q.add_columns(Organization)
        .options(selectinload(Organization.activity))
        .where(Organization.title.ilike(f"%{name}%"))
    )
    return q
