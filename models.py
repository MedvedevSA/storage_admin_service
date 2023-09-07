from datetime import datetime

from sqlalchemy import TIMESTAMP, func, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import ProgrammingError

from database import Base, engine


class StorageItemsCategories(Base):
    __tablename__ = "storageitems_categories"
    storage_item_id: Mapped[int] = mapped_column(
        ForeignKey("storage_items.id", ondelete='CASCADE'), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete='CASCADE'), primary_key=True
    )


class StorageItems(Base):
    __tablename__ = "storage_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    time_created: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now()
    )
    time_updated: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now()
    )
    categories: Mapped[list["StorageItemsCategories"]] = relationship(
        "Categories", secondary="storageitems_categories",
        back_populates="storage_items", lazy='subquery'
    )


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )

    time_created: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now()
    )
    time_updated: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now()
    )
    storage_items: Mapped[list["StorageItemsCategories"]] = relationship(
        "StorageItems", secondary="storageitems_categories",
        back_populates="categories", lazy='subquery'
    )


async def chech_or_init_db(clean_db=False):
    async with engine.begin() as conn:
        if clean_db:
            await conn.run_sync(Base.metadata.drop_all)
        try:
            await conn.execute(select(Categories).limit(1))
        except ProgrammingError:
            await conn.run_sync(Base.metadata.create_all)

