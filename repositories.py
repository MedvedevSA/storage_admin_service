import logging
from typing import Any

from sqlalchemy import delete, insert, select, update

from database import Base, async_session
from models import StorageItem, Category, JournalLog, ItemField, FieldValue
from select_generator import Dump, SelectGenerator

logger = logging.getLogger("uvicorn")


class SQLAlchemyRepository:
    model: Base

    async def add_one_m2m(
        self,
        parent_data: dict,
        relations: list[dict[str, dict]]
    ):
        async with async_session() as session:
            parent = self.model(**parent_data)
            session.add(parent)
            await session.commit()
            for relation in relations:
                for relation_fld, data in relation.items():
                    try:
                        annotated: dict = data['meta']
                        
                        for child_id in data['children']:
                            session.add(
                                annotated['associate'](
                                    **{
                                        annotated['parent_fk']: parent.id,
                                        annotated['child_fk']: child_id,
                                    }
                                )
                            )
                    except KeyError:
                        logger.error('m2m key err')
                        await session.rollback()
                    except AttributeError:
                        logger.error('m2m attr err')
                        await session.rollback()

            await session.commit()
            return parent.id

    async def update_one_m2m(self, parent_id: Any, parent_data: dict, relations: list[dict]):
        async with async_session() as session:
            stmt = update(self.model).where(
                self.model.id == parent_id
            ).values(**parent_data).returning(self.model.id)
            await session.execute(stmt)
            await session.commit()
            for data in relations:
                annotated: dict = data['meta']
                del_stmt = delete(annotated['associate']).where(
                    getattr(annotated['associate'], annotated['parent_fk']) == parent_id
                )
                await session.execute(del_stmt)
                
                for child_id in data['children']:
                    session.add(
                        annotated['associate'](
                            **{
                                annotated['parent_fk']: parent_id,
                                annotated['child_fk']: child_id,
                            }
                        )
                    )
            await session.commit()
            return parent_id

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


class FieldValueRepository(SQLAlchemyRepository):
    model = FieldValue


class ItemFieldRepository(SQLAlchemyRepository):
    model = ItemField


class StorageItemsRepository(SQLAlchemyRepository):
    model = StorageItem


class CategoriesRepository(SQLAlchemyRepository):
    model = Category


class JournaLogRepository(SQLAlchemyRepository):
    model = JournalLog
