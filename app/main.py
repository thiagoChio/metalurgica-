"""Ponto de entrada da aplicacao."""

import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import api, pages

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def create_app() -> FastAPI:
    application = FastAPI(
        title="Site institucional - Metalurgica",
        docs_url="/api/docs" if settings.debug else None,
        redoc_url=None,
    )
    application.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
    application.include_router(pages.router)
    application.include_router(api.router)
    return application


app = create_app()
