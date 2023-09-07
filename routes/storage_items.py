from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import StorageItemsRepository
from schemas import AddStorageItem, UpdStorageItem, StorageItem, StorageItemFilter
from services import BaseService
from utils import module_url

r = APIRouter()
BASE = module_url(__name__)


def service_depends():
    return BaseService(StorageItemsRepository)


ServiceDepends = Annotated[BaseService, Depends(service_depends)]


@r.post(BASE)
async def add_storage_item(
    item: AddStorageItem,
    storage_items_srvc: ServiceDepends
) -> int | None:
    return await storage_items_srvc.add_one_m2m(item)


@r.get(BASE)
async def get_storage_items(
    filters: Annotated[StorageItemFilter, Depends()],
    storage_items_srvc: ServiceDepends
) -> list[StorageItem]:
    return await storage_items_srvc.get_all(
        params=filters, response_model=StorageItem
    )


@r.get(BASE + '/{id}')
async def get_storage_item(
    id: int,
    storage_items_srvc: ServiceDepends
) -> StorageItem | None:
    return await storage_items_srvc.get_one(id, response_model=StorageItem)


@r.put(BASE + '/{id}')
async def update_storage_item(
    id: int,
    upd_item: UpdStorageItem,
    storage_items_srvc: ServiceDepends
) -> int:
    return await storage_items_srvc.update_one(id, upd_item)


@r.delete(BASE + '/{id}')
async def delete_storage_item(
    id: int,
    storage_items_srvc: ServiceDepends
) -> int:
    return await storage_items_srvc.del_one(id)
