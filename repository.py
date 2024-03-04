from db import session, ImagesORM
from schemas import ImageAdd, Image
from sqlalchemy import select


class ImageRep:
    @classmethod
    async def add_image(cls, data: ImageAdd):
        async with session() as sesi:
            image_dict = data.model_dump()
            image = ImagesORM(**image_dict)
            sesi.add(image)
            await sesi.flush()
            await sesi.commit()
            return image

    @classmethod
    async def get_images(cls) -> list[Image]:
        async with session() as sesi:
            query = select(ImagesORM)
            res = await sesi.execute(query)
            images = res.scalars().all()
            return images
