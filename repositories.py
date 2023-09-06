from typing import Any

from sqlalchemy import delete, insert, select, update

from database import Base, async_session
from models import StorageItems
from select_generator import Dump, SelectGenerator


class SQLAlchemyRepository:
    model: Base

    async def add_one(self, data: dict):
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_one(self, id: Any):
        async with async_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            return (await session.execute(stmt)).scalar()

    async def update_one(self, id: Any, data: dict):
        async with async_session() as session:
            stmt = update(self.model).where(
                self.model.id == id
            ).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()

    async def get_all(self, params: Dump = None, relations: dict = None):
        async with async_session() as session:
            stmt = SelectGenerator(self.model, params, relations).get_stmt()
            return (await session.execute(stmt)).scalars()

    async def del_one(self, id):
        async with async_session() as session:
            stmt = delete(self.model).where(
                self.model.id == id
            ).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()


class StorageItemsRepository(SQLAlchemyRepository):
    model = StorageItems
