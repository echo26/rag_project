import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from logging_config import setup_logging
from router.chat import router as chat_router
from router.health import router as health_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    setup_logging()
    logger.info("startup complete")
    yield
    logger.info("shutting down")


app = FastAPI(lifespan=lifespan)

app.include_router(chat_router)
app.include_router(health_router)
