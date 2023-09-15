from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apps.core.config import REDIS_CONF,JOBS_KEY,RUN_TIMES_KEY,ASYNC_REDIS_URL,REDIS_LOCK_CONNECTION_DETAILS
import multiprocessing,logging,functools,os
from redlock import RedLock, RedLockError



workers = multiprocessing.cpu_count() * 2 + 1





# Schedule = None
init_schedule = {
            # 配置存储器
            'jobstores': {
                # 'default': SQLAlchemyJobStore(url=DATABASE_URL),
                'default': RedisJobStore(jobs_key=JOBS_KEY, run_times_key=RUN_TIMES_KEY, **REDIS_CONF),
            },
            # 配置执行器,使用进程池调度
            'executors': {
                # 'default': ProcessPoolExecutor(workers),
                'default': ThreadPoolExecutor(max_workers=workers*2),
                'processpool': ProcessPoolExecutor(max_workers=workers)
            },
            # 创建 job 时的默认参数
            'job_defaults': {
                'coalesce': True,  # 如果系统因为某些原因没有执行任务，导致任务累计，为True只运行一次，False则累计的任务全部跑一遍
                'max_instances': workers, # 允许并发运行最大实例数
            },
            'timezone': 'Asia/Shanghai'
        }

Schedule = AsyncIOScheduler(**init_schedule)


async def start_scheduler():
    # global Schedule
    try:
        Schedule.start()
        logging.info("Created Schedule Object")   
    except Exception as e:
        logging.error(str(e))     
        logging.error("Unable to Create Schedule Object")       






async def shutdown_scheduler():
    # global Schedule
    try:
        Schedule.shutdown()
        logging.info("Disabled Schedule")
    except Exception as e:
        logging.error(str(e))     
        logging.error("Unable to Disabled Schedule Object")     
    







'''abscheduler封装'''


# 封装 Scheduler
class Scheduler(object):
    scheduler: AsyncIOScheduler = None


    @staticmethod
    def init(scheduler):
        Scheduler.scheduler = scheduler

    @staticmethod
    def configure(**kwargs):
        Scheduler.scheduler.configure(**kwargs)


    @staticmethod
    async def start():
        Scheduler.scheduler.start()


    @staticmethod
    def add(**kwargs):
        pass


    @staticmethod
    def edit():
        pass

    @staticmethod
    def pause(id, status):
        """
        暂停或恢复测试计划, 会影响到next_run_at
        :param plan_id:
        :param status:
        :return:
        """
        if status:
            Scheduler.scheduler.resume_job(job_id=str(id))
        else:
            Scheduler.scheduler.pause_job(job_id=str(id))

    @staticmethod
    def remove(id):
        Scheduler.scheduler.remove_job(id)

    @staticmethod
    def list():
        job_list = Scheduler.scheduler.get_jobs()
        return job_list


    @staticmethod
    async def shutdown():
        Scheduler.scheduler.shutdown(wait=False) # 将 wait 选项设置为 False 可以立即关闭。



    ## 计划任务分布式锁
    @staticmethod
    def lock(key):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    # 使用语句/上下文管理器， 试图获取分布式锁，如果没有获取到则会抛出RedLockError，所以我们这里捕获它
                    # 关于唯一key的确认，我这边首先加上了distributed_lock的前缀，是因为方便区分其他key，接着通过函数名称+唯一key确认分布式key，
                    # 但由于有的方法是带参数的，所以我选择再加一个args，来支持那些同方法不同参数的任务。
                    # 只需要在方法加上 lock 这个装饰器即可
                    with RedLock(f"distributed_lock:{func.__name__}:{key}:{str(args)}", connection_details=REDIS_LOCK_CONNECTION_DETAILS):
                        return await func(*args, **kwargs)
                except RedLockError:
                    logging.debug(f"进程: {os.getpid()}获取任务失败, 不用担心，还有其他哥们给你执行了")

            return wrapper

        return decorator