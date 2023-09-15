from pydantic import BaseModel,Field
from typing import List,Optional
from enum import Enum


class EnableStatus(Enum):
    enable  = 1
    disable = 0


class CreateSchema(BaseModel):
    roleName: str
    roleCode: str
    enable: int
    sort: int
    details: str

class UpdateSchema(CreateSchema):
    roleId: int



class UpdateEnableSchema(BaseModel):
    id: int


class BatchDeleteSchema(BaseModel):
    ids: Optional[list[int]] = []



class BindingSchema(BaseModel):
    roleId: int
    powerIds: Optional[list[int]] = []