from typing import Annotated, AsyncGenerator
from fastapi import Depends, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from db import pg_async_session


async def add_secret_to_header(
    secret: Annotated[str, Header(alias="X-Api-Key")],
) -> str:
    """Функция добавляет secret в header"""

    return secret


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """в модуле
    from sqlalchemy.ext.asyncio import AsyncSession

    def _get(db: Annotated[AsyncSession, Depends(get_session)]):
        ...
    """
    async with pg_async_session() as _session:
        yield _session


class Pagination:
    def __init__(
        self, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, max=1000)
    ):
        self.offset = offset
        self.limit = limit

    @property
    def dict(self):
        return {"offset": self.offset, "limit": self.limit}
