from datetime import datetime
from typing import Literal

from fastapi import Query
from pydantic import BaseModel, computed_field


class SortingModel(BaseModel):
    sort_col: str | None = Query(default=None)
    sort_order: Literal['asc', 'desc'] = Query(default='asc')


class PagingModel(BaseModel):
    page_number: int = Query(default=1)
    page_limit: int = Query(default=100, ge=1, le=1000)

    @computed_field
    @property
    def offset(self) -> int:
        return (self.page_number - 1) * self.page_limit


class AddStorageItem(BaseModel):
    name: str


class UpdStorageItem(AddStorageItem):
    ...


class StorageItem(AddStorageItem):
    id: int
    time_created: datetime
    time_updated: datetime
