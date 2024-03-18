from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData
from typing import Optional
import asyncio
import aiomysql


URL_DATABASE = (
    'postgresql+asyncpg://bobr:Kurwa_Perdole@127.0.0.1:5432/pg_images_db'
)

#URL_DATABASE = (
#    'mysql+aiomysql://bobr:Kurwa_Perdole@127.0.0.1:5432/mysql_images_db?charset=utf8mb4'
#)

engine = create_async_engine(URL_DATABASE, future=True, echo=True)
# ('sqlite+aiosqlite:///images.db')

db_session = async_sessionmaker(engine, expire_on_commit=False)


#loop = asyncio.get_event_loop()
#
#async def connection():
#    conn = await aiomysql.connect(host='127.0.0.1', port=5432,
#                                  user='root', password='Kurwa_Perdole',
#                                  db='mysql_images_db', loop=loop)


class Base(DeclarativeBase):
    pass


class ImagesORM(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)  # index=True
    name: Mapped[Optional[str]]
    image: Mapped[Optional[bytes]]
    byte_image_size: Mapped[Optional[float]]
    width: Mapped[Optional[int]]
    height: Mapped[Optional[int]]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
