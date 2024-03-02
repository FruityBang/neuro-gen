from fastapi import APIRouter
from models import CreateImage, SendImage
from db import async_session, ImageDAL

v1_router = APIRouter(prefix='/v1/image')


async def _get_new_image(body: CreateImage) -> SendImage:
    async with async_session() as session:
        async with session.begin():
            image_dal = ImageDAL(session)
            image = await image_dal.create_image(name=body.title,
                                                 title=body.title)
            return SendImage(title=image.title, name=image.name)


@v1_router.post('/', response_model=SendImage)
async def get_image(body: CreateImage) -> SendImage:
    return await _get_new_image(body)
