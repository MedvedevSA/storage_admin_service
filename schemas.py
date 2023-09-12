from typing import Annotated, Literal
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, computed_field, ConfigDict, Field
from models import Category, StorageItemCategory, ItemTypes


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


class AddCategory(BaseModel):
    name: str
    parent_id: None | int = Field(gt=0)


class UpdCategory(AddCategory):
    ...


class BaseCategory(AddCategory):
    model_config = ConfigDict(from_attributes=True)

    id: int
    time_created: datetime
    time_updated: datetime


class AddStorageItem(BaseModel):
    name: str
    categories: Annotated[list[int], dict(
        associate=StorageItemCategory,
        parent_fk='storage_item_id', child_fk='category_id'
    )]


class UpdStorageItem(AddStorageItem):
    ...


class UpdItemField(BaseModel):
    name: str


class AddItemField(UpdItemField):
    type: ItemTypes


class BaseItemField(AddItemField):
    id: int


class BaseStorageItem(AddStorageItem):
    model_config = ConfigDict(from_attributes=True)

    id: int
    time_created: datetime
    time_updated: datetime
    categories: list[BaseCategory]


class StorageItemFilter(BaseModel):
    model_config = ConfigDict(relation_prefix={
        '_': StorageItemCategory, 'category': Category
    })

    category__id__in: list[int] | None = Field(Query(default=[]))
    name__ilike: str | None = Query(default=None)


class JournalLog(BaseModel):
    id: int
    client_ip: str
    data: dict
    time_created: datetime
