from fastapi import APIRouter, Request, Depends,UploadFile, File, Body
from apps.common.temp import templates
from apps.depends.manager import manager
from apps.depends.route_auth import authorize_and_log, authorize
from apps.api.admin.services.FileServices import Service
from apps.api.admin.schemas.FileSchemas import DeleteSchema,BatchDeleteSchema
from apps.common.query_params import FilterParamsMixin
from apps.common.reponse import APIResponse



router = APIRouter()





#                               ----------------------------------------------------------
#                               -------------------------  视图层 --------------------------
#                               ----------------------------------------------------------

@router.get("/")
@authorize_and_log("admin:file:main")
async def index(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin/photo/photo.html", {"request": request, "authorize": authorize, "current_user": user})



@router.get("/upload")
@authorize_and_log("admin:file:add")
async def upload(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin/photo/photo_add.html", {"request": request})



#                               ----------------------------------------------------------
#                               -------------------------  API接口 --------------------------
#                               ----------------------------------------------------------


#  图片数据
@router.get('/table')
# @authorize_and_log("admin:file:main")
async def gettable(request: Request, params: FilterParamsMixin = Depends(), user=Depends(manager)):
    result, count = await Service.list(page=params.page, limit=params.limit)
    return APIResponse(data={
        'msg': "",
        'code': 0,
        'result': result,
        'count': count,
    })


# 图片上传
@router.post("/upload")
@authorize_and_log("admin:file:add")
async def upload(request: Request, file: UploadFile = File(...), user=Depends(manager)):
    file_url = await Service.upload_one(photo=file, mime=file.content_type)
    return APIResponse(data={"src": file_url}, msg='上传成功')



# 图片删除
@router.post('/delete')
@authorize_and_log("admin:file:delete")
async def delete(request: Request, item: DeleteSchema, user=Depends(manager)):
    await Service.delete_photo_by_id(item.id)
    return APIResponse(msg='删除成功')


# 图片删除
@router.post('/batchRemove')
@authorize_and_log("admin:file:delete")
async def delete(request: Request, item: BatchDeleteSchema,  user=Depends(manager)):
    await Service.batchRemove(item.ids)
    return APIResponse(msg='批量删除成功')