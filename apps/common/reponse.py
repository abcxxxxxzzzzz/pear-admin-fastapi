from fastapi.responses import ORJSONResponse,JSONResponse


CODE = dict({
    10000: "参数校验错误,请检查提交的参数信息",
    10001: "未经许可授权",
    10002: "当前访问没权限!",
    10003: "访问地址不存在",
    10004: "不允许使用此方法提交访问",
    10005: "文件数量过多",
    10006: "文件扩展名不符合规范",
    10007: "访问的速度过快",
    10008: "未知的其他HTTPEOOER异常",
    10009: "服务崩溃异常"
})




class APIResponse(JSONResponse):
    
    http_status_code = 200  # 定义返回响应码--如果不指定的话则默认都是返回200
    code = 1                # 默认成功
    data = None             # 结果可以是 {} 或 []
    success = True
    msg = 'success'

    def __init__(self, http_status_code=None, code=1, success=None, data=None, msg=None, **options):

        if  code != self.code:
            self.success = False
        if http_status_code:
            self.http_status_code = http_status_code
        if code:
            self.code = code
        if data:
            self.data = data
        if msg:
            self.msg = msg
        # if success is not None:
        #     self.success = success
        

        # 返回内容体
        body = dict(
            msg=self.msg,
            code=self.code,
            success=self.success,
            data=self.data,
        )
        super(APIResponse, self).__init__(status_code=self.http_status_code, content=body, **options)