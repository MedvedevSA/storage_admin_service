from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, engine


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


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
