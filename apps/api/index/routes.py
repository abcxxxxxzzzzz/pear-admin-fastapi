
from pydantic import BaseModel,Field
from fastapi import APIRouter


class IndexSchema(BaseModel):
    name: str =  Field(..., title='名称', description='表述', min_length=2, max_length=10)




router = APIRouter()

@router.get('/')
def index(name: IndexSchema):
    return name