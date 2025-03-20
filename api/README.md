# Тестовое приложение

# 

### Переменные окружения

* PG_HOST
* PG_PORT
* PG_DB
* PG_USER
* PG_PASSWORD

### Команды для разработки

* Запуск сервиса: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
* Применить актуальные миграции: `docker compose exec web alembic upgrade head  `
* Сгенерировать новую миграцию `alembic revision --autogenerate -m "<msg>"`
* Откатить миграцию на одну назад `alembic downgrade -1`

---

WORK DIR: ./src
PYTHONUNBUFFERED=1;PYTHONDONTWRITEBYTECODE=1

## Установка pre-commit хука для автоматического поднятия версии при git commit

```commandline
cp pre-commit ./.git/hooks/pre-commit
```
