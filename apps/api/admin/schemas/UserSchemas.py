from pydantic import BaseModel,Field
from typing import List,Optional
from enum import Enum


class EnableStatus(Enum):
    enable  = 1
    disable = 0


class BaseSchema(BaseModel):
    username: str = Field(..., max_length=20)
    realname: str = Field(..., max_length=20)
    # avatar:   Optional[str] = None
    # remark:   Optional[str] = None
    enable:   EnableStatus = EnableStatus.disable.value
    # dept_id:  Optional[int] = None
    role:     List[int] = []

        




class CreateSchema(BaseSchema):
    password: str = Field(..., min_length=3, max_length=50)


    



class UpdatePwdSchema(BaseModel):
    oldpassword: str
    password: str = Field(..., min_length=3, max_length=50)
    repassword: str = Field(..., min_length=3, max_length=50)



class UpdateEnableSchema(BaseModel):
    id: int


class BatchDeleteSchema(BaseModel):
    ids: Optional[list[int]] = []


class UpdateDataSchema(BaseModel):
    userId: int
    realName: str
    roleIds: Optional[List[int]] = []