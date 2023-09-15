from fastapi import APIRouter, Request, Depends
from sqlalchemy import desc
from fastapi_sqlalchemy import db
from fastapi.encoders import jsonable_encoder
from apps.depends.manager import manager
from apps.common.temp import templates
from apps.api.admin.models import AdminLog
from apps.depends.route_auth import  authorize_and_log
from apps.common.reponse import APIResponse
from apps.core.config import TOKEN_URL


router = APIRouter()

#                               ----------------------------------------------------------
#                               -------------------------  日志管理 --------------------------
#                               ----------------------------------------------------------

@router.get("/")
@authorize_and_log("admin:log:main")
async def index(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin/admin_log/main.html", {"request": request})



#                               ==========================================================
#                                                            登录日志
#                               ==========================================================

@router.get("/loginLog")
@authorize_and_log("admin:log:main")
async def getLoginLog(request: Request, page: int, limit: int, user=Depends(manager)):
    log =  db.session.query(AdminLog).filter_by(url = TOKEN_URL).order_by(desc(AdminLog.create_time)).offset((page-1)*limit).limit(limit).all()
    count = db.session.query(AdminLog).filter_by(url = TOKEN_URL).count()
    output = jsonable_encoder(log)
    res = {
        'msg': "",
        'code': 0,
        'result': output,
        'count': count,
        'limit': "10"

    }
    return APIResponse(data=res)

#                               ==========================================================
#                                                            操作日志
#                               ==========================================================

@router.get("/operateLog")
@authorize_and_log("admin:log:main")
async def getLoginLog(request: Request, page: int, limit: int, user=Depends(manager)):
    log =  db.session.query(AdminLog).filter(AdminLog.url != TOKEN_URL).order_by(desc(AdminLog.create_time)).offset((page-1)*limit).limit(limit).all()
    count = db.session.query(AdminLog).filter(AdminLog.url != TOKEN_URL).count()
    output = jsonable_encoder(log)
    res = {
        'msg': "",
        'code': 0,
        'data': output,
        'count': count,
        'limit': "10"

    }
    return APIResponse(data=res)