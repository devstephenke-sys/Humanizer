from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.config import get_settings

settings = get_settings()


def normalize_database_url(url: str) -> tuple[str, dict]:
    """Return an async SQLAlchemy URL and engine kwargs.

    Neon strings often arrive as postgresql://...?sslmode=require.
    asyncpg does not accept libpq's sslmode query argument, so SSL is passed
    as a connect argument instead.
    """
    raw = url.strip()
    if raw.startswith("postgres://"):
        raw = "postgresql://" + raw[len("postgres://") :]
    kwargs: dict = {}
    if raw.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
        if ":memory:" in raw or raw.endswith("sqlite+aiosqlite://"):
            kwargs["poolclass"] = StaticPool
        return raw, kwargs

    ssl_required = "sslmode=require" in raw or "ssl=require" in raw
    if raw.startswith("postgresql://"):
        raw = "postgresql+asyncpg://" + raw[len("postgresql://") :]
    if raw.startswith("postgresql+asyncpg://"):
        base, _, query = raw.partition("?")
        if query:
            kept = [
                part
                for part in query.split("&")
                if part and not part.startswith("sslmode=") and not part.startswith("ssl=")
            ]
            raw = base + (("?" + "&".join(kept)) if kept else "")
        else:
            raw = base
        if ssl_required or "neon.tech" in raw:
            kwargs["connect_args"] = {"ssl": True}
    return raw, kwargs


database_url, engine_kwargs = normalize_database_url(settings.database_url)
engine = create_async_engine(database_url, **engine_kwargs)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
