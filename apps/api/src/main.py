import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from db.pool import pool
from logging_config import configure_logging
from routers.chat import router as chat_router
from routers.health import router as health_router
from routers.search import router as search_router
from services.llm import LlmError

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    async with pool.connection() as conn:
        await conn.execute("SELECT 1")
    yield
    await pool.close()


configure_logging()

app = FastAPI(lifespan=lifespan)
# Matches any localhost port since Vite's dev port isn't fixed (5173, 5174, ...).
# Add the production frontend origin explicitly once Phase 6 (deployment) lands.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http://localhost:\d+$",
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(health_router)


@app.exception_handler(LlmError)
async def llm_error_handler(request: Request, exc: LlmError) -> JSONResponse:
    logger.error("LLM provider error", exc_info=exc)
    return JSONResponse(
        status_code=503,
        content={"detail": "The AI provider is currently unavailable."},
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}