from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from settings import DATABASE_URL
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False,
                             class_=AsyncSession)

Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'

    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)


class ImageDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_image(self, title, name) -> Image:
        new_image = Image(title=title, name=name)
        self.db_session.add(new_image)
        await self.db_session.flush()
        return new_image
