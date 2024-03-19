"""Module with db models."""
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

load_dotenv()

URL_DATABASE = os.getenv('URL_DB')

engine = create_async_engine(URL_DATABASE, future=True, echo=True)

db_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class ImagesORM(Base):
    """Sqlalchemy images model."""
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)  # index=True
    name: Mapped[Optional[str]]
    image: Mapped[Optional[bytes]]
    byte_image_size: Mapped[Optional[float]]
    width: Mapped[Optional[int]]
    height: Mapped[Optional[int]]


async def create_tables():
    """Developing moment."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    """Developing moment."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
