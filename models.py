from enum import Enum
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, engine


class ItemTypes(Enum):
    str = 'str'
    int = 'int'
    float = 'float'


class StorageItemCategory(Base):
    __tablename__ = "storage_item__category"
    storage_item_id: Mapped[int] = mapped_column(
        ForeignKey("storage_item.id", ondelete='CASCADE'), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete='CASCADE'), primary_key=True
    )


class StorageItem(Base):
    __tablename__ = "storage_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    time_created: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now
    )
    time_updated: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now, onupdate=datetime.now
    )
    categories: Mapped[list["StorageItemCategory"]] = relationship(
        "Category", secondary="storage_item__category",
        back_populates="storage_items", lazy='subquery'
    )


class ItemField(Base):
    __tablename__ = "item_field"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[ItemTypes]

    field_values: Mapped[list['FieldValue']] = relationship(
        back_populates='item_field'
    )


class FieldValue(Base):
    __tablename__ = "field_value"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    item_field_id: Mapped[int] = mapped_column(
        ForeignKey(ItemField.id, ondelete='CASCADE')
    )
    storage_item_id: Mapped[int] = mapped_column(
        ForeignKey(StorageItem.id, ondelete='CASCADE')
    )
    item_field: Mapped[ItemField] = relationship(back_populates='field_values')


UniqueConstraint(FieldValue.item_field_id, FieldValue.storage_item_id)


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete='SET NULL'), nullable=True
    )

    time_created: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now
    )
    time_updated: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now, onupdate=datetime.now
    )
    storage_items: Mapped[list["StorageItemCategory"]] = relationship(
        "StorageItem", secondary="storage_item__category",
        back_populates="categories", lazy='subquery'
    )


class JournalLog(Base):
    __tablename__ = "journal_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_ip: Mapped[str]
    data: Mapped[dict] = mapped_column(JSON)
    time_created: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
