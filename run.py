"""Atalho para desenvolvimento: `python run.py` sobe o site com reload."""

import uvicorn

from app.config import settings

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)
