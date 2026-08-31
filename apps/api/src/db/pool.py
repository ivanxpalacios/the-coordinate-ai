from pgvector.psycopg import register_vector_async
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

from config import settings


async def _configure(conn: AsyncConnection) -> None:
    await register_vector_async(conn)


# open=False: the pool is opened explicitly in main.py's lifespan, so
# connections are established on app startup, not on module import.
pool = AsyncConnectionPool(
    conninfo=settings.database_url,
    configure=_configure,
    open=False,
)