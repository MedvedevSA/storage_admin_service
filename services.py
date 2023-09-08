from typing import TypeVar

from pydantic import BaseModel

from repositories import SQLAlchemyRepository

Model = TypeVar('Model', bound='BaseModel')
ParamsModel = TypeVar('ParamsModel', bound='BaseModel')
ResponseModel = TypeVar('ResponseModel', bound='BaseModel')


class BaseService:
    def __init__(self, repository: type[SQLAlchemyRepository]):
        self.repository = repository()

    async def add_one_m2m(self, obj: Model) -> int:
        parent = obj.model_dump(exclude_unset=True)
        relations = list()
        for fld, info in type(obj).model_fields.items():
            if info.metadata:
                relations.append({fld: {
                        'meta': info.metadata[0],
                        'children': parent.pop(fld),
                    }
                })

        return await self.repository.add_one_m2m(parent, relations)

    async def update_one_m2m(self, id: int, obj: Model) -> int:
        parent = obj.model_dump(exclude_unset=True)
        relations = list()
        for fld, info in type(obj).model_fields.items():
            if info.metadata:
                relations.append({
                        'meta': info.metadata[0],
                        'children': parent.pop(fld),
                    }
                )

        return await self.repository.update_one_m2m(
            id, parent, relations
        )

    async def add_one(self, obj: Model) -> int:
        return await self.repository.add_one(
            obj.model_dump(exclude_unset=True)
        )

    async def get_one(
        self,
        id: int,
        response_model: ResponseModel
    ) -> ResponseModel | None:
        row = await self.repository.get_one(id)
        if row:
            return response_model.model_validate(row)

    async def get_all(
            self,
            params: ParamsModel = None,
            response_model: type[ResponseModel] = None
    ) -> list[ResponseModel]:
        relations = None
        if params:
            relations = params.model_config.get('relation_prefix')
            params = {
                k: v
                for k, v
                in params.model_dump().items()
                if v not in [None, []]
            }
        rows = await self.repository.get_all(params, relations)
        return [
            response_model.model_validate(row, from_attributes=True)
            for row
            in rows
        ]

    async def update_one(self, id: int, obj: Model) -> int:
        return await self.repository.update_one(
            id, obj.model_dump()
        )

    async def patch_one(self, id: int, obj: Model) -> int:
        return await self.repository.update_one(
            id, obj.model_dump(exclude_unset=True)
        )

    async def del_one(self, id: int) -> int:
        return await self.repository.del_one(id)
