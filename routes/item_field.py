from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import ItemFieldRepository
from schemas import AddItemField, BaseItemField, UpdItemField
from services import BaseService
from utils import module_url

r = APIRouter()
BASE = module_url(__name__)


def service_depends():
    return BaseService(ItemFieldRepository)


ServiceDepends = Annotated[BaseService, Depends(service_depends)]


@r.post(BASE)
async def add_item_field(
    item_field: AddItemField,
    item_field_srvc: ServiceDepends
) -> int | None:
    return await item_field_srvc.add_one(item_field)


@r.get(BASE)
async def get_item_fields(
    item_field_srvc: ServiceDepends
) -> list[BaseItemField]:
    return await item_field_srvc.get_all(response_model=BaseItemField)


@r.get(BASE + '/{id}')
async def get_item_field(
    id: int,
    item_field_srvc: ServiceDepends
) -> BaseItemField | None:
    return await item_field_srvc.get_one(id, response_model=BaseItemField)


@r.put(BASE + '/{id}')
async def update_item_field(
    id: int,
    upd_item_field: UpdItemField,
    item_field_srvc: ServiceDepends
) -> int | None:
    return await item_field_srvc.update_one(id, upd_item_field)


@r.delete(BASE + '/{id}')
async def delete_item_field(
    id: int,
    item_field_srvc: ServiceDepends
) -> int:
    return await item_field_srvc.del_one(id)
