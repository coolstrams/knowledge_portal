from contextlib import asynccontextmanager
from app.core.redis import redis_client


@asynccontextmanager
async def lifespan(app):
    redis_client.ping()
    print("✅ Redis connected")
    yield
