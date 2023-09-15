from typing import Optional
from fastapi import Query
from pydantic import BaseModel

class PaginateConst:
    DefaultNum = 1
    DefaultSize = 10

    MinNum = 1
    MaxSize = 40



class FilterParamsMixin(BaseModel):
    """search list data"""

    page: Optional[int] = Query(PaginateConst.DefaultNum, title='page', gte=PaginateConst.MinNum)
    limit: Optional[int] = Query(PaginateConst.DefaultSize, title='limit', gte=1, lte=PaginateConst.MaxSize)