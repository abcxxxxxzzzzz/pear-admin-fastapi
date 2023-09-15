from fastapi import Request, Response,HTTPException
from apps.common.reponse import APIResponse



class BaseException(HTTPException):
    http_state_code = 500       # 接口正常，200
    msg = '服务器内部未定义错误'
  
    def __init__(self, msg=None, http_state_code = http_state_code):
        if http_state_code:
            self.http_state_code = http_state_code
        if msg:
            self.msg = msg
        raise HTTPException(status_code=self.http_state_code, detail=self.msg)



async def http_exception_handler(request: Request, exc: BaseException) -> Response:
    return APIResponse(code=exc.status_code, msg=exc.detail)



