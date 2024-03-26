"""Module providing db methods V2."""
from fastapi import HTTPException
import sqlalchemy.orm
from transliterate import translit
from db import db_session, ImagesORM
from V2_api.V2_schemas import Images, ImagesAdd
from generate import generate_image


class ImagesRep:
    @classmethod
    async def get_images(cls, data: ImagesAdd) -> Images:
        """
        Retrieves image data from the database based on provided parameters.
        """
        try:
            async with db_session() as session:
                images_dict = data.model_dump()
                if data.name:
                    query = sqlalchemy.orm.Query(
                        ImagesORM, session=session
                        ).filter(ImagesORM.name == images_dict['name'])
                    result = await session.execute(query)
                    ex_images = result.scalars().one_or_none()
                    return ex_images
                query = sqlalchemy.orm.Query(
                    ImagesORM, session=session
                    ).filter(ImagesORM.id == data.id)
                result = await session.execute(query)
                ex_images = result.scalars().one_or_none()
                return ex_images
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"DB error man: '{error}'"
            )

    @classmethod
    async def add_images(cls, data: ImagesAdd) -> Images:
        """Generates and adds image data to the database."""
        try:
            async with db_session() as session:
                images_dict = data.model_dump()
                query = sqlalchemy.orm.Query(
                    ImagesORM, session=session
                    ).filter(ImagesORM.title == images_dict['title'])
                result = await session.execute(query)
                ex_images = result.scalars().one_or_none()
                if ex_images:
                    print(f'ex={ex_images}')
                    return ex_images
                name = translit(
                    images_dict['title'], 'ru', reversed=True
                    ).lower().replace(' ', '_')
                images_dict['name'] = name + '.png'
                images_data = (generate_image(images_dict['title']))
                if isinstance(images_data, str):
                    return images_data
                byte_image, byte_image_size_kB, width, height = images_data
                images_dict['images'] = byte_image
                images_dict['byte_image_size_kB'] = byte_image_size_kB
                images_dict['width'] = width
                images_dict['height'] = height
                images = ImagesORM(**images_dict)
                session.add(images)
                await session.flush()
                await session.commit()
                return images
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"DB error man: '{error}'"
            )
