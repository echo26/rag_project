from fastapi import FastAPI

from router.chat import router as chat_router
from router.health import router as health_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(health_router)
