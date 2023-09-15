from pydantic import BaseModel,Field
from typing import List,Optional
from enum import Enum


class EnableStatus(Enum):
    enable  = 1
    disable = 0

class CreateSchema(BaseModel):
    icon: str
    title: str
    parent_id: int
    type: int
    code: str
    open_type: str
    href: str
    sort: int
    enable: EnableStatus = EnableStatus.enable.value


class UpdateSchema(CreateSchema):
    id: int



class UpdateEnableSchema(BaseModel):
    id: int


class BatchDeleteSchema(BaseModel):
    ids: Optional[list[int]] = []


# class UpdateDataSchema(BaseModel):
#     userId: int
#     realName: str
#     roleIds: Optional[List[int]] = []