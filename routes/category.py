from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import CategoriesRepository
from schemas import AddCategory, UpdCategory, Category
from services import BaseService
from utils import module_url

r = APIRouter()
BASE = module_url(__name__)


def service_depends():
    return BaseService(CategoriesRepository)


ServiceDepends = Annotated[BaseService, Depends(service_depends)]


@r.post(BASE)
async def add_category(
    category: AddCategory,
    category_srvc: ServiceDepends
) -> int | None:
    return await category_srvc.add_one(category)


@r.get(BASE)
async def get_categories(
    category_srvc: ServiceDepends
) -> list[Category]:
    return await category_srvc.get_all(response_model=Category)


@r.get(BASE + '/{id: int}')
async def get_category(
    id: int,
    category_srvc: ServiceDepends
) -> Category | None:
    return await category_srvc.get_one(id, response_model=Category)


@r.put(BASE + '/{id: int}')
async def update_category(
    id: int,
    upd_category: UpdCategory,
    category_srvc: ServiceDepends
) -> int:
    return await category_srvc.update_one(id, upd_category)


@r.delete(BASE + '/{id: int}')
async def delete_category(
    id: int,
    category_srvc: ServiceDepends
) -> int:
    return await category_srvc.del_one(id)
