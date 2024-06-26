import json
import logging
from typing import Any

from redis.asyncio import from_url, Redis

logger = logging.getLogger(__name__)

Connection = Redis


async def init(config: dict) -> Connection:

    logger.info("Create redis pool")

    dsn = config.get('dsn')
    if not dsn:
        raise RuntimeError('Redis connection parameters not defined')
    maxsize = config.get('maxsize', 10)

    return from_url(
        dsn,
        max_connections=maxsize
    )


async def close(pool: Connection):
    await pool.close()


async def get(key: str, conn: Connection) -> dict | None:
    data = await conn.get(key)
    if data is not None:
        try:
            return json.loads(data)
        except:
            logger.exception(f'Wrong session data {data}')
    return None


async def set(key: str, value: Any, conn: Connection):
    await conn.set(key, json.dumps(value))


async def del_(key: str, conn: Connection):
    await conn.delete(key)


async def setex(key: str, ttl: int, value: Any, conn: Connection):
    await conn.setex(key, ttl, json.dumps(value))
