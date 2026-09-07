import logging

import psycopg
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from db.pool import pool

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health() -> JSONResponse:
    try:
        async with pool.connection() as conn:
            await conn.execute("SELECT 1")
    except psycopg.Error as e:
        logger.error("Health check failed: database unreachable", exc_info=e)
        return JSONResponse(
            status_code=503,
            content={"detail": "Database connection unavailable."},
        )
    return JSONResponse(status_code=200, content={"status": "ok"})
