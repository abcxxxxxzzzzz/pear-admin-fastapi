from fastapi import APIRouter
from apps.api.index.routes import router as IndexRouter
from apps.api.admin.routes import router as AdminRouter


router = APIRouter()


router.include_router(IndexRouter, tags=['index'])
router.include_router(AdminRouter, prefix='/admin')