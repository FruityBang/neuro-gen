from db import new_session, ImagesORM
from schemas import ImageAdd, Image
from sqlalchemy import select
from transliterate import translit
import sqlalchemy.orm


class ImageRep:
    @classmethod
    async def get_images(cls, ex_image) -> Image:
#        async with new_session() as session:
#            query = select(ImagesORM)
#            res = await session.execute(query)
#            images = res.scalars().all()
        return ex_image

    @classmethod
    async def add_image(cls, data: ImageAdd):
        async with new_session() as session:
            image_dict = data.model_dump()
            query = sqlalchemy.orm.Query(
                ImagesORM, session=session
                ).filter(ImagesORM.title == image_dict['title'])
            result = await session.execute(query)
            ex_image = result.scalars().one_or_none()
            if ex_image:
                return ex_image
            name = translit(
                image_dict['title'], 'ru', reversed=True
                ).lower().replace(' ', '_')
            image_dict['name'] = name + '.png'
            image = ImagesORM(**image_dict)
            session.add(image)
            await session.flush()
            await session.commit()
            return image
