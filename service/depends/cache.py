
from fastapi import Request
from misc.redis import Connection


async def get(request: Request) -> Connection:
    try:
        pool = request.app.state.redis
    except AttributeError:
        raise RuntimeError("App state has no redis pool")
    else:
        async with pool as conn:
            yield conn
