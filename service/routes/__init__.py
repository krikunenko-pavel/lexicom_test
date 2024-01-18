from fastapi import FastAPI
from . import addresses


def register_routes(app: FastAPI):
    app.include_router(addresses.router)
    return app



