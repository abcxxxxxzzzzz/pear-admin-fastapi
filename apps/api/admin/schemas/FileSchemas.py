from pydantic import BaseModel
from typing import Optional, List



class DeleteSchema(BaseModel):
    id: int

class BatchDeleteSchema(BaseModel):
    ids: Optional[List[int]] = []
