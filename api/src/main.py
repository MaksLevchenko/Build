import logging
from fastapi import FastAPI
import uvicorn
from config.settings import settings
from config.loger_config import loger_init
from organizations.handlers import router as router_organization

loger_init()
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Тестовое задание",
    version=settings.app_version,
    redoc_url=None,
    docs_url=settings.app_swagger_url,
    root_path=settings.app_root_path,
)


@app.get("/")
async def healthcheck():
    return {
        "title": app.title,
        "version": app.version,
    }


app.include_router(router_organization, prefix="/organizations", tags=["Организации"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
