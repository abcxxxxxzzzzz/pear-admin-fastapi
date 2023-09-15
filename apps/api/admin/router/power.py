from apps.depends.manager import manager
from fastapi import APIRouter, Request, Depends
from apps.depends.route_auth import authorize, authorize_and_log
from apps.common.temp import templates
from apps.api.admin.services.PowerServices import Service
from apps.common.reponse import APIResponse
from apps.api.admin.schemas.PowerSchemas import (
    CreateSchema,UpdateSchema,UpdateEnableSchema,BatchDeleteSchema
)


router = APIRouter()


'''
视图
'''


@router.get("/")
@authorize_and_log("admin:power:main")
async def index(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin/power/main.html", {"request": request, "authorize": authorize, "current_user": user})



@router.get("/data")
@authorize_and_log("admin:power:main")
async def data(request: Request, user=Depends(manager)):
    result = await Service.list()
    return APIResponse(data=result)

# 增加
@router.get("/add")
@authorize_and_log("admin:power:add")
async def add(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin/power/add.html", {"request": request})



# 权限编辑
@router.get('/edit/{id}')
@authorize_and_log("admin:power:edit")
async def edit(request: Request,id: int,  user=Depends(manager)):
    power = await Service.get_by_id(id)
    icon = str(power.icon).split()
    if len(icon) == 2:
        icon = icon[1]
    else:
        icon = None
    return templates.TemplateResponse("admin/power/edit.html", {"request": request, "power": power, "icon": icon})


@router.get('/selectParent')
@authorize_and_log("admin:power:add")
async def selectParent(request: Request, user=Depends(manager)):
    power_data = await Service.select_parent()
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": power_data

    }
    return res





# 增加
@router.post("/save")
@authorize_and_log("admin:power:add")
async def save(request: Request, item: CreateSchema ,user=Depends(manager)):
    result = await Service.add(item)
    return APIResponse(msg='添加成功', data=result)


# 权限角色
@router.put('/update')
@authorize_and_log("admin:power:edit")
async def update(request: Request,item: UpdateSchema, user=Depends(manager)):
    await Service.update(item)
    return APIResponse(msg='更新权限成功')


# 启用权限
@router.put('/enable')
@authorize_and_log("admin:power:edit")
async def enable(request: Request, item: UpdateEnableSchema, user=Depends(manager)):
    await Service.enable_status(item.id)
    return APIResponse(msg='启动成功')

# 禁用权限
@router.put('/disable')
@authorize_and_log("admin:power:edit")
async def disenable(request: Request, item: UpdateEnableSchema, user=Depends(manager)):
    await Service.disable_status(item.id)
    return APIResponse(msg='禁用成功')

# 角色删除
@router.delete('/remove/{id}')
@authorize_and_log("admin:power:remove")
async def remove(request: Request,id: int,  user=Depends(manager)):
    await Service.delete_by_id(id)
    return APIResponse(msg='删除成功')

# 批量删除
@router.delete('/batchRemove')
@authorize_and_log("admin:power:remove")
async def remove(request: Request, item: BatchDeleteSchema, user=Depends(manager)):
    await Service.batch_remove(item.ids)
    return {"msg": "批量删除成功", "success": True}