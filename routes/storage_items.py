from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import StorageItemsRepository
from schemas import AddStorageItem
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
    return await storage_items_srvc.add_one(item)

