from starlette.config import Config
from sqlalchemy.pool import NullPool

config = Config(".env")


DEBUG: bool = config("DEBUG", cast=bool, default=False)


# APP模块
APP_MODELS = [
    'apps.api.admin.models'
]

# 密钥
SECRET_KEY: str = config('SECRET_KEY', cast=str)
KEY_EXPIRES = 1.0

# TOKEN 登录路径
TOKEN_URL: str = config('TOKEN_URL', cast=str)



# 静态文件路径||模板路径
STATIC_PATH: str = config('STATIC_PATH', cast=str)
STATIC_DIR: str = config('STATIC_DIR', cast=str)
STATIC_NAME: str = config('STATIC_NAME', cast=str)
TEMPLATES_DIR: str = config('TEMPLATES_DIR', cast=str)

# 图片存储路径
UPLOAD_PATH = f'{STATIC_DIR}/upload/'


# Mysql 数据库
DB_HOST: str = config("DB_HOST", cast=str)
DB_USER: str = config("DB_USER", cast=str)
DB_PASS: str = config("DB_PASS", cast=str)
DB_NAME: str = config("DB_NAME", cast=str)
DB_PORT: str = config("DB_PORT", cast=str)
DATABASE_URL =  f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
ENGINE_ARGS = {'pool_recycle': 60*5, 'pool_pre_ping': True, 'poolclass': NullPool}


# Redis 数据库
REDIS_HOST: str = config("REDIS_HOST", cast=str)
REDIS_USER: str = config("REDIS_USER", cast=str)
REDIS_PASS: str = config("REDIS_PASS", cast=str)
REDIS_DB: str = config("REDIS_DB", cast=str)
REDIS_PORT: str = config("REDIS_PORT", cast=str)
ASYNC_REDIS_URL = f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8&decode_responses=True"


# Redis分布式锁
REDIS_LOCK_CONNECTION_DETAILS = [{
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': REDIS_DB,
    'password': REDIS_PASS,
}]


# APScheduler 任务调度器
REDIS_CONF = REDIS_LOCK_CONNECTION_DETAILS[0]
JOBS_KEY      = 'apscheduler.jobs'
RUN_TIMES_KEY = 'apscheduler.run_times'

