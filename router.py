from base64 import b64encode
from fastapi import APIRouter, HTTPException
from repository import ImageRep
from schemas import Image, ImageAdd


v1_router = APIRouter(prefix='/v1/image', tags=['images'])


@v1_router.post('')
async def send_image(image: ImageAdd) -> Image:
    if image.title:
        image_data = await ImageRep.add_image(image)
        if isinstance(image_data, str):
            raise HTTPException(
                status_code=400,
                detail=f"Kandinsky says: '{image_data}'"
            )
        image_data.image = b64encode(image_data.image).decode('utf-8')
        return image_data

    elif image.name:
        ex_image = await ImageRep.get_image(image)
        if not ex_image:
            raise HTTPException(
                status_code=404,
                detail='Image DOES NOT exist dear'
                )
        ex_image.image = b64encode(ex_image.image).decode('utf-8')
        return ex_image
    elif image.id:
        ex_image = await ImageRep.get_image(image)
        if not ex_image:
            raise HTTPException(
                status_code=404,
                detail='Image DOES NOT exist dear'
                )
        ex_image.image = b64encode(ex_image.image).decode('utf-8')
        return ex_image
    raise HTTPException(
        status_code=400,
        detail=(
            "'title' or 'name' or 'id' field are not in request BUT should be"
            )
        )


# @v1_router.get('')
# async def get_images() -> list[Image]:
#     images = await ImageRep.get_images()
#     return images
