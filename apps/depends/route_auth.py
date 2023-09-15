from apps.api.admin.services.AdminLogServices import admin_log
from functools import wraps

from fastapi import HTTPException
from apps.depends.mem_session import mem_session
from typing import Optional
from apps.common.reponse import APIResponse

def authorize(power: str, user):
    if not power in mem_session.get(user.username, []):
        return False
    return True



def authorize_and_log(power: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            request = kwargs.get('request')
            print(request)

            if not power in mem_session.get(user.username, []):
                admin_log(request=request, uid=user.id, is_access=False)
                raise HTTPException(status_code=403, detail='权限不足')
            admin_log(request=request, uid=user.id, is_access=True)
            return await func(*args, **kwargs)
        return wrapper
    return decorator