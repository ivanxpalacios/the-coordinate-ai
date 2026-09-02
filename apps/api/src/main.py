from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.pool import pool
from logging_config import configure_logging
from routers.chat import router as chat_router
from routers.search import router as search_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    async with pool.connection() as conn:
        await conn.execute("SELECT 1")
    yield
    await pool.close()


configure_logging()

app = FastAPI(lifespan=lifespan)
app.include_router(search_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}