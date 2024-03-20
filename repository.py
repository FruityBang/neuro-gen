"""Module providing db methods."""
from fastapi import HTTPException
import sqlalchemy.orm
from transliterate import translit
from db import db_session, ImagesORM
from generate import generate_image
from schemas import Image, ImageAdd


class ImageRep:
    @classmethod
    async def get_image(cls, data: ImageAdd) -> Image:
        """
        Retrieves image data from the database based on provided parameters.
        """
        try:
            async with db_session() as session:
                image_dict = data.model_dump()
                if data.name:
                    query = sqlalchemy.orm.Query(
                        ImagesORM, session=session
                        ).filter(ImagesORM.name == image_dict['name'])
                    result = await session.execute(query)
                    ex_image = result.scalars().one_or_none()
                    return ex_image
                query = sqlalchemy.orm.Query(
                    ImagesORM, session=session
                    ).filter(ImagesORM.id == data.id)
                result = await session.execute(query)
                ex_image = result.scalars().one_or_none()
                return ex_image
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"DB error man: '{error}'"
            )

    @classmethod
    async def add_image(cls, data: ImageAdd) -> Image:
        """Generates and adds image data to the database."""
        try:
            async with db_session() as session:
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
                image_data = (generate_image(image_dict['title']))
                if isinstance(image_data, str):
                    return image_data
                byte_image, byte_image_size, width, height = image_data
                image_dict['image'] = byte_image
                image_dict['byte_image_size'] = byte_image_size
                image_dict['width'] = width
                image_dict['height'] = height
                image = ImagesORM(**image_dict)
                session.add(image)
                await session.flush()
                await session.commit()
                return image
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"DB error man: '{error}'"
            )
