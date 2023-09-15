from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from apps.core.event import create_start_app_handler,create_stop_app_handler
from apps.errors.http_error import http_exception_handler
from apps.errors.validation_error import validation_exception_handler
from apps.api.routes import router as api_router
from apps.core.config import STATIC_PATH,STATIC_DIR,STATIC_NAME,DATABASE_URL,ENGINE_ARGS
from apps.depends.manager import auth_exception_handler,NotAuthenticatedException





def get_application() -> FastAPI:
    application = FastAPI(title='我的测试项目', debug=True, version='1.0.0')


    # 全局跨域设置    
    application.add_middleware(
        CORSMiddleware,
        allow_origins= ['*'],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )

    # databases global
    application.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL, engine_args=ENGINE_ARGS)


    # 全局的启动和关闭事件
    application.add_event_handler('startup', create_start_app_handler(application))
    application.add_event_handler('shutdown', create_stop_app_handler(application))
    
    # 全局异常捕获信息 （Pydanic 422 验证异常触发器， HTTP 请求异常触发器, Fastapi-login 令牌失效）
    application.add_exception_handler(RequestValidationError, validation_exception_handler) 
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(NotAuthenticatedException, auth_exception_handler)

    # 挂载静态文件
    application.mount(STATIC_PATH, StaticFiles(directory=STATIC_DIR), name=STATIC_NAME)

    # 路由
    application.include_router(api_router, prefix='')

    return application

    

app = get_application()


