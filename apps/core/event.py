from fastapi import FastAPI
from typing import Callable
from .nosql import redis_pool
from .scheduler import start_scheduler, shutdown_scheduler





def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await redis_pool()
        await start_scheduler()
    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await shutdown_scheduler()
        # pass
    return stop_app