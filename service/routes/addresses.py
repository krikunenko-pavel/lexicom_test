from fastapi import (
    APIRouter,
    Depends
)

from service.models import (
    CheckDataModel,
    WriteDataModel,
    Result
)

from service.depends import cache
from misc import redis as cache_funcs


router = APIRouter(
    tags=["Addresses"]
)


@router.get("/check_data", response_model=Result)
async def check_data(
        data: CheckDataModel = Depends(),
        redis_conn: cache_funcs.Connection = Depends(cache.get)
):
    return Result(
        result=f"{await cache_funcs.get(data.phone, redis_conn)}"
    )


@router.post("/write_data", response_model=Result)
async def write_data(
        data: WriteDataModel,
        redis_conn: cache_funcs.Connection = Depends(cache.get)
):

    await cache_funcs.setex(data.phone, 3600 * 24 * 7, data.address, redis_conn)

    return Result(result="Ok")