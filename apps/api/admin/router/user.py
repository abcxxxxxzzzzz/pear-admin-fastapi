from apps.api.admin.models import Role
from fastapi import APIRouter, Request, Depends, Body
from apps.common.temp import templates
from apps.depends.manager import manager
from apps.api.admin.services.UserServices import Service
from apps.common.reponse import APIResponse
from apps.common.query_params import FilterParamsMixin
from apps.api.admin.schemas.UserSchemas import (
    CreateSchema,UpdateEnableSchema,UpdatePwdSchema,BatchDeleteSchema,UpdateDataSchema
)

from fastapi_sqlalchemy import db
from apps.depends.route_auth import authorize, authorize_and_log

# from app.services.route_auth import authorize_and_log, authorize




router = APIRouter()


'''
视图
'''

# view: 主页
@router.get("/")
@authorize_and_log("admin:user:main")
async def index(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin/user/main.html", {"request": request, "authorize": authorize, "current_user": user})


# view: 增加
@router.get("/add")
@authorize_and_log("admin:user:add")
async def add(request: Request, user=Depends(manager)):
    roles = db.session.query(Role).all()
    return templates.TemplateResponse("admin/user/add.html", {"request": request, "roles": roles})


# view: 编辑
@router.get('/edit/{id}')
@authorize_and_log("admin:user:edit")
async def edit(request: Request,id: int,  user=Depends(manager)):
    user = await Service.get_by_id(id)
    roles = db.session.query(Role).all()
    checked_roles = []
    for r in user.role:
        checked_roles.append(r.id)
    return templates.TemplateResponse("admin/user/edit.html", {"request": request, "user": user, "roles": roles, "checked_roles": checked_roles})




# '''
# API接口
# '''



# API: 表格数据
@router.get('/data')
@authorize_and_log("admin:user:main")
async def getData(request: Request,  realName: str=None, username: str=None,  params: FilterParamsMixin = Depends(), user=Depends(manager)):
    filters = {}
    if realName:
        filters["realname"] = ('%' + realName + '%')
    if username:
        filters["username"] = ('%' + username + '%')
    result, count = await Service.list(params, filters)
    return APIResponse(data={
        'code': 0,
        'msg': "",
        'count': count,
        'result' : result,
    })

# API: 增加
@router.post("/save")
@authorize_and_log("admin:user:add")
async def save(request: Request, item: CreateSchema,user=Depends(manager)):
    result = await Service.add(item)
    return APIResponse(data=result)


# API: 角色
@router.put('/update')
@authorize_and_log("admin:user:edit")
async def update(request: Request,item: UpdateDataSchema, user=Depends(manager)):
    return APIResponse(msg='更新成功')


# API: 启用
@router.put('/enable')
@authorize_and_log("admin:user:edit")
async def enable(request: Request, item: UpdateEnableSchema, user=Depends(manager)):
    await Service.enable_status(item.id)
    return APIResponse(msg='启动成功')

# API: 禁用
@router.put('/disable')
@authorize_and_log("admin:user:edit")
async def disenable(request: Request, item: UpdateEnableSchema, user=Depends(manager)):
    # id = dict(await request.json()).get('userId')

    await Service.disable_status(item.id)
    return APIResponse(msg='禁用成功')

# API: 用户删除
@router.delete('/remove/{id}')
@authorize_and_log("admin:user:remove")
async def remove(request: Request,id: int,  user=Depends(manager)):
    await Service.delete_by_id(id)
    return APIResponse(msg='删除成功')

# API: 批量删除
@router.delete('/batchRemove')
@authorize_and_log("admin:user:remove")
async def remove(request: Request, item: BatchDeleteSchema, user=Depends(manager)):
    # ids = (await request.form()).getlist("ids[]")
    await Service.batch_remove(item.ids)
    return APIResponse(msg='批量删除成功')