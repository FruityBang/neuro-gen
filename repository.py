from db import new_session, ImagesORM
from schemas import ImageAdd, Image
from sqlalchemy import select
from transliterate import translit
import sqlalchemy.orm
from generate import generate_image


class ImageRep:
    @classmethod
    async def get_images(cls, ex_image) -> Image:
# async with new_session() as session:
# query = select(ImagesORM)
# res = await session.execute(query)
# images = res.scalars().all()
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
#            image_dict['image'] = open('byteimage.png', 'rb').read()
#            image_dict['image'] = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x08\x00\x00\x00\x08\x08\x02\x00\x00\x00Km)\xdc\x00\x00\x00\x19IDATx\x9cb\x11ox\xcd\x80\r0a\x15\x1d\xb4\x12\x80\x00\x00\x00\xff\xff3'\x01\x95\xc4\x15\x00|\x00\x00\x00\x00IEND\xaeB`\x82"
            byte_image, byte_image_size, width, height = (
                generate_image(image_dict['title']))
            image_dict['image'] = byte_image
            image_dict['byte_image_size'] = byte_image_size
            image_dict['width'] = width
            image_dict['height'] = height
            image = ImagesORM(**image_dict)
            session.add(image)
            await session.flush()
            await session.commit()
            return image
