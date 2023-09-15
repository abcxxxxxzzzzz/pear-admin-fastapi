import logging
import aioredis
import functools
from redlock import RedLock, RedLockError
import os
from apps.core.config import ASYNC_REDIS_URL





async def redis_pool(db: int=0):
    '''
    redis链接池
    :return
    '''

    redis = await aioredis.from_url(
        # redis://[[username]:[password]]@localhost:6379/0
        # f"redis://:{redis_config.get('password')}@{redis_config.get('host')}/{db}?encoding=utf-8"
        # redis://127.0.0.1", port=44117, password='qwaszx', db=2, encoding="utf-8", decode_responses=True
        ASYNC_REDIS_URL
    )
    return redis




# # 分布式加锁
# def redis_lock(key: str):
#     def decorator(func):
#         @functools.wraps(func)
#         async def wrapper(*args, **kwargs):
#             try:
#                 # print(func.__name__, key, args)
#                 # 试图获取分布式锁，如果没有获取到则会抛出RedLockError，所以我们这里捕获它
#                 with RedLock(f"distributed_lock:{func.__name__}:{key}:{str(args)}",
#                              connection_details=REDIS_LOCK_CONNECTION_DETAILS,
#                              ):
#                     return await func(*args, **kwargs)
#             except RedLockError:
#                 logging.debug(f"进程: {os.getpid()}获取任务失败, 不用担心，还有其他哥们给你执行了")
#                 print(f"进程: {os.getpid()}获取任务失败, 不用担心，还有其他哥们给你执行了")

#         return wrapper

#     return decorator




'''Redis常规操作'''

from fastapi import Request
from typing import Optional


async def setToRedis(request: Request, key: str, value: str, expire: Optional[int] = 0):
    if expire:
        await request.app.state.redis.set(key, value, ex=expire)
    else:
        await request.app.state.redis.set(key, value)


async def getFoRedis(request: Request, key: str):
    return await request.app.state.redis.get(key)



async def removeFoRedis(request: Request, key: str):
    return await request.app.state.redis.delete(key)