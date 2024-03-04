from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


engine = create_async_engine(
    'sqlite+aiosqlite:///images.db'
)

session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class ImagesORM(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    name: Mapped[Optional[str]]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
