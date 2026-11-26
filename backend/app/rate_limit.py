import time
from collections import defaultdict

from fastapi import HTTPException, Request

from app.config import get_settings


class RateLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, list[float]] = defaultdict(list)

    def check(self, key: str, limit: int, window_seconds: int) -> None:
        now = time.monotonic()
        recent = [stamp for stamp in self._hits[key] if now - stamp < window_seconds]
        if len(recent) >= limit:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Wait a few minutes and try again. This limit applies to everyone and is not a paid plan.",
            )
        recent.append(now)
        self._hits[key] = recent


limiter = RateLimiter()


def client_key(request: Request, bucket: str) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "local")
    return f"{bucket}:{ip}"


def enforce_write_limit(request: Request, bucket: str) -> None:
    settings = get_settings()
    limiter.check(client_key(request, bucket), settings.rate_limit_writes, settings.rate_limit_window_seconds)
