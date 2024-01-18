from fastapi import FastAPI

from service.models import ErrorResponse
from service.routes import register_routes
from service.state import State
import logging
from misc import (
    redis,
    error_handlers,
    config
)

logger = logging.getLogger(__name__)


def factory() -> FastAPI:
    app = FastAPI()

    app.state = State(conf=config.read_config())

    register_startup(app)
    register_shutdown(app)

    register_routes(app)
    # error_handlers.register_exception_handler(app)
    return app


def register_startup(app: FastAPI):
    @app.on_event("startup")
    async def handler_startup():
        try:
            await startup(app)
        except:
            logger.exception("Startup crashed")

    return app


async def startup(app: FastAPI):
    app.state.redis = await redis.init(app.state.conf.get('redis'))
    return app


def register_shutdown(app: FastAPI):
    @app.on_event("shutdown")
    async def handler_shutdown():
        try:
            await shutdown(app)
        except:
            logger.exception("Shutdown crashed")

    return app


async def shutdown(app: FastAPI):

    if app.state.redis:
        await redis.close(app.state.redis)

    return app


def responses():
    return {
        400: {
            "model": ErrorResponse
        },
        401: {
            "model": ErrorResponse
        },
        404: {
            "model": ErrorResponse
        },
        422: {
            "model": ErrorResponse
        },
        500: {
            "model": ErrorResponse
        },
    }
