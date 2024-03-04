from fastapi import APIRouter
from schemas import ImageAdd, Image
from repository import ImageRep

v1_router = APIRouter(prefix='/v1/image', tags=['images'])


@v1_router.post('')
async def send_image(image: ImageAdd) -> Image:
    image = await ImageRep.add_image(image)
    return image


@v1_router.get('')
async def get_images() -> list[Image]:
    images = await ImageRep.get_images()
    return images
