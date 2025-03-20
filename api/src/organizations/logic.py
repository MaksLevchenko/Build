from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from config.settings import settings


API_KEY = settings.secret_api_key


def get_all_children(obj) -> list[str]:
    """Возвращает имена всех наследников класса"""

    childrens_name = []

    current_obj = obj

    while current_obj:
        childrens_name.append(current_obj.title)
        current_obj = current_obj.children
    return childrens_name


def verify_key(api_key):
    """Проверяет ключ доступа к API"""
    if api_key != API_KEY:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Ключ не верный!")
