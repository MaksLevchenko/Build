# Тестовое приложение

# Клонируйте проект командой: `git clone https://github.com/MaksLevchenko/Build.git`

## Переименнуйте файл local.env.dev в local.env и присвойте переменным внутри него актуальные данные

### Переменные окружения

* pg_db
* pg_password
* secret_api_key

## В терминале перейдите в папку src командой `cd /api/src`

# При запущеном docker descktop выполните команду: `docker-compose build`

# После окончания сборки контейнера выполните: `docker-compose up -d`

# Затем нужно применить миграции. Для этого выполните команду: `docker compose exec web alembic upgrade head`

### Теперь перейдите в браузере по адресу: `http://127.0.0.1:8000/docs#/`

### Осталось только заполнить базу данных. Это можно сделать выполнив самый нижний роут, или перейти по адресу: `http://127.0.0.1:8000/organizations/fill-the-database/`
