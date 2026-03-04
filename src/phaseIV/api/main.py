from contextlib import asynccontextmanager
from fastapi import FastAPI

from phaseIV.scrapper.client import PhaseivClient
from phaseIV.api.routes import router
from phaseIV.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create one shared PhaseivClient for the lifetime of the server."""

    app.state.client = PhaseivClient(
        timeout=settings.http_timeout,
        cache_dir=settings.cache_dir,
        cache_enabled=settings.cache_enabled,
    )
    yield
    await app.state.client.close()


app = FastAPI(
    title="PhaseIV Film Library API",
    description="REST API for scraping the Phase IV film lending library.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)
