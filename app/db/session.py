# (c) Danit Consultancy and Development, January-2026, danittech@yahoo.com

""" Async database session management """

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# ----------------------------------------------------------------------------------------

# The engine is the low-level connection pool to PostgreSQL.
# echo=False means SQL statements are not printed to the console.
# It is created once at module import time and shared across all requests.
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# ----------------------------------------------------------------------------------------

# async_sessionmaker is a factory that produces AsyncSession objects.
# expire_on_commit=False means ORM objects remain usable after a commit
# (important in async code where lazy loading is not available).
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ----------------------------------------------------------------------------------------

async def get_db():
    """
    FastAPI dependency that yields an AsyncSession per request.

    Usage in an endpoint:
        async def my_endpoint(db: AsyncSession = Depends(get_db)):
            ...

    The `async with` block ensures the session is always closed after the
    request completes, even if an exception is raised.
    """
    async with AsyncSessionLocal() as session:
        yield session
