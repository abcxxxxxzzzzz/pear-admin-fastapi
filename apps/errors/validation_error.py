from fastapi import Request,HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError 
from typing import Union
import logging
from  apps.common.reponse import APIResponse


_any_error = {
    'value_error.jsondecode': '传入的参数字段出现转换错误，请核对是否存在类型错误',
    'value_error.missing': '{loction} 类型 {name} 参数字段为必传参数',
    'value_error.any_str.max_length': '{loction} 类型 {name} 参数字段字符串长度最多{limit_value}位',
    'value_error.any_str.min_length': '{loction} 类型 {name} 参数字段字符串长度至少{limit_value}位以上',
    'value_error.number.not_gt': '{loction} 类型 {name} 参数字段信息必须大于{limit_value}',
    'value_error.number.not_le': '{loction} 类型 {name} 参数字段信息必须小于等于{limit_value}',
    # =============================================
    # type_error.none.not_allowed
    'type_error.none.not_allowed': '{loction} 类型 {name} 参数字段值必须不能空值',
    "type_error.integer": "{loction} 类型 {name} 参数必须是一个int类型的参数",
    "type_error.float": "{loction} 类型 {name} 参数必须是一个float类型的参数",
}



async def validation_exception_handler(request: Request, exc: Union[RequestValidationError, ValidationError]):
    _error = f'{exc.body} --> {[err.get("loc") for err in exc.errors()]}'
    logging.error(_error)

    undefined = "{loction} type for: {name} is: {meessage} ,error type is：{errortypr}"

    status_code = getattr(exc, 'status_code', 400)
    status_msg  = ''
    try:
        for err in exc.errors():

            ''' 转换错误时'''
            if err["type"] == 'value_error.jsondecode':
                err["msg"] = _any_error[err["type"]]
                return err["msg"]
            

            loction = err["loc"][0]    # 错误字段的位置,错误类型
            name = err["loc"][1]       # 错误字段名称



            '''长度'''
            _value = None
            try:
                _value = err['ctx']
            except:
                pass

            limit_value = None
            if _value and 'limit_value' in _value:
                limit_value = _value['limit_value']

            if limit_value:
                status_msg = _any_error[err["type"]].format(loction=loction,name=name,limit_value=limit_value) if err["type"] in _any_error else \
                            undefined.format(loction=loction, name=name, meessage=err["msg"], errortypr=err["type"])
            else:
                status_msg = _any_error[err["type"]].format(loction=loction, name=name) if err[ "type"] in _any_error else \
                            undefined.format(loction=loction, name=name, meessage=err["msg"], errortypr=err["type"])
        return APIResponse(code=status_code, msg=status_msg)
    except:
        return APIResponse(code=status_code, msg=_error)
    