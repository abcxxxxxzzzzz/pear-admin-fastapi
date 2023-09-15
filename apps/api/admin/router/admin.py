from fastapi import APIRouter, Request, Form,Depends
from apps.common.temp import templates
from apps.api.admin.utils.MakeCaptchaTools import get_captcha
from apps.common.trees import make_menu_tree
from apps.common.reponse import APIResponse
from apps.depends.mem_session import mem_session
from apps.api.admin.services.UserServices import Service
from apps.depends.manager import manager




router = APIRouter()


'''View 视图'''

@router.get("/")
async def index(request: Request, user=Depends(manager)):
    '''
       后台根页面
    '''
    realname = user.realname
    return templates.TemplateResponse("admin/index.html", {"request": request, "realname": realname})


@router.get("/login")
async def login(request: Request):
    '''
        登录页面
    '''
    return templates.TemplateResponse("admin/login.html", {"request": request})


@router.get('/welcome')
def welcome(request: Request, user=Depends(manager)):
    '''
        登录后控制台页面
    '''
    return templates.TemplateResponse('admin/console/console.html', {"request": request})






# -------------------------------------------------------------------------------------------------


'''
    API 接口
'''


# 获取验证码API
@router.get("/getCaptcha")
async def getCaptcha():
    resp, code = get_captcha()
    mem_session[code] = code
    return resp



# 登录接口API
@router.post('/login')
async def login(request: Request, 
                    username: str=Form(...), 
                    password: str=Form(...), 
                    captcha: str=Form(...)
                ):
    
    return await Service.CheckLoginForm(request,username, password, captcha)



# 获取登录用户菜单
@router.get("/menu")
async def getMenu(user=Depends(manager)):
    menu = make_menu_tree(user)
    return menu


# 退出登录
@router.post("/logout")
async def logout(user=Depends(manager)):
    # response = JSONResponse(content={"msg":"注销成功","success":True})
    response = APIResponse(msg='注销成功')
    manager.set_cookie(response, "null")
    return response



