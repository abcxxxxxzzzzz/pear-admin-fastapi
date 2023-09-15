from apps.api.admin.models import AdminLog
from fastapi import APIRouter, Request, Depends
from sqlalchemy import desc
from fastapi_sqlalchemy import db
from apps.common.temp import templates
from apps.depends.manager import manager
from apps.depends.route_auth import authorize, authorize_and_log
from apps.api.admin.services.RoleServices import Service
from apps.common.query_params import FilterParamsMixin
from apps.common.reponse import APIResponse
from apps.api.admin.schemas.RoleSchemas import (
    CreateSchema,UpdateSchema,UpdateEnableSchema,BatchDeleteSchema,BindingSchema
)



router = APIRouter()



#                               ----------------------------------------------------------
#                               -------------------------  视图层 --------------------------
#                               ----------------------------------------------------------

@router.get("/")
@authorize_and_log("admin:role:main")
async def index(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin/role/main.html", {"request": request, "authorize": authorize, "current_user": user})


# 角色增加
@router.get("/add")
@authorize_and_log("admin:role:add")
async def add(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin/role/add.html", {"request": request})



# 角色编辑
@router.get('/edit/{id}')
@authorize_and_log("admin:role:edit")
async def edit(request: Request, id: int,  user=Depends(manager)):
    role = await Service.get_by_id(id)
    return templates.TemplateResponse("admin/role/edit.html", {"request": request, "role": role})


# 角色授权
@router.get('/power/{id}')
@authorize_and_log("admin:role:power")
async def getPower(request: Request,id: int,  user=Depends(manager)):
    return templates.TemplateResponse("admin/role/power.html", {"request": request, "id": id})


#                               ----------------------------------------------------------
#                               -------------------------  API接口 --------------------------
#                               ----------------------------------------------------------

# 表格数据
@router.get("/data")
@authorize_and_log("admin:role:main")
async def getData(request: Request, params: FilterParamsMixin = Depends(), roleName: str=None, roleCode: str=None, user=Depends(manager)):
    filters = {}
    if roleName:
        filters["name"] = ('%' + roleName + '%')
    if roleCode:
        filters["code"] = ('%' + roleCode + '%')
    result, count = await Service.list(params=params, filters=filters)
    return APIResponse(data={
        'code': 0,
        'msg': "",
        'count': count,
        'result' : result,
    })



# 角色增加
@router.post("/save")
@authorize_and_log("admin:role:add")
async def save(request: Request, item: CreateSchema, user=Depends(manager)):
    await Service.add(item)
    return APIResponse(msg='添加成功')



# 角色授权
@router.get('/getRolePower/{id}')
@authorize_and_log("admin:role:main")
async def getRolePower(request: Request,id: int,  user=Depends(manager)):
    powers = await Service.get_role_power(id)
    res = {
        "data": powers,
        "status": {"code": 200, "message": "默认"}
    }
    return res

# 保存角色权限
@router.put('/saveRolePower')
@authorize_and_log("admin:role:edit")
async def saveRolePower(request: Request, item: BindingSchema,  user=Depends(manager)):
    await Service.update_role_power(id=item.roleId, power_list=item.powerIds)
    return APIResponse(msg='授权成功')



# 更新角色
@router.put('/update')
@authorize_and_log("admin:role:edit")
async def update(request: Request, item: UpdateSchema,user=Depends(manager)):
    await Service.update(item)
    return APIResponse(msg='更新角色成功')

# 启用用户
@router.put('/enable')
@authorize_and_log("admin:role:edit")
async def enable(request: Request,  item: UpdateEnableSchema, user=Depends(manager)):
    await Service.enable_status(item.id)
    return APIResponse(msg='启动成功')


# 禁用用户
@router.put('/disable')
@authorize_and_log("admin:role:edit")
async def disenable(request: Request,  item: UpdateEnableSchema, user=Depends(manager)):
    await Service.disable_status(item.id)
    return APIResponse(msg='禁用成功')


# 角色删除
@router.delete('/remove/{id}')
@authorize_and_log("admin:role:remove")
async def remove(request: Request, id: int,  user=Depends(manager)):
    await Service.delete_by_id(id)
    return APIResponse(msg='角色删除成功')

# 批量删除
@router.delete('/batchRemove')
@authorize_and_log("admin:role:remove")
async def remove(request: Request, item: BatchDeleteSchema,user=Depends(manager)):
    await Service.batch_remove(item.ids)
    return APIResponse(msg='批量删除成功')
