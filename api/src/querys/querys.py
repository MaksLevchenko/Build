from pydantic import BaseModel
from sqlalchemy import delete, select, func, insert, update
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert

# from db.models import Book
from db import Base, pg_async_session


def add_new_model(schema: BaseModel, model: Base):
    q = insert(model).values(schema.model_dump())
    return q


def delete_model_by_id(id: int, model: Base):
    q = delete(model).where(model.id == id)
    return q


def update_model_q(model: Base, schema: BaseModel):
    print(schema.model_dump())
    q = update(model).where(model.id == schema.id).values(**schema.model_dump())
    return q
