from fastapi import APIRouter
from apps.api.admin.router.admin import router as LoginRouter
from apps.api.admin.router.user import router as UserRouter
from apps.api.admin.router.power import router as PowerRouter
from apps.api.admin.router.monitor import router as MonitorRouter
from apps.api.admin.router.admin_log import router as AdminLoGRouter
from apps.api.admin.router.role import router as RoleRouter
from apps.api.admin.router.file import router as FileRouter

router = APIRouter()


router.include_router(LoginRouter, tags=['Login'])
router.include_router(UserRouter, tags=['Admin:User'], prefix='/user')
router.include_router(PowerRouter, tags=['Admin:Power'], prefix='/power')
router.include_router(MonitorRouter, tags=['Admin:Monitor'], prefix='/monitor')
router.include_router(MonitorRouter, tags=['Admin:Monitor'], prefix='/monitor')
router.include_router(AdminLoGRouter, tags=["Admin:AdminLoG"], prefix="/log")
router.include_router(RoleRouter, tags=["Admin:Role"], prefix="/role")
router.include_router(FileRouter, tags=["Admin:File"], prefix="/file")

