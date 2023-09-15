from fastapi import Request,status
from tortoise.exceptions import BaseORMException
from  apps.common.reponse import APIResponse


'''tortoise orm 异常处理'''
async def business_exception_handler(request: Request, error: BaseORMException):

    import logging 
    logging.error(str(error))
    return APIResponse(
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        msg='服务器繁忙，请稍后再试'
    )
