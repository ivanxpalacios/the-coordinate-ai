import pytest_asyncio

from db.pool import pool


@pytest_asyncio.fixture(scope="session", autouse=True)
async def open_pool():
    await pool.open(wait=True)
    yield
    await pool.close()
