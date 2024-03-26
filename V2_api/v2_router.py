"""Endpoint handler V2."""
from base64 import b64encode
from fastapi import APIRouter, HTTPException
from V2_api.V2_repository import ImagesRep
from V2_api.V2_schemas import Images, ImagesAdd


v2_router = APIRouter(prefix='/v2/images', tags=['V2_images'])


@v2_router.post('')
async def send_images(images: ImagesAdd) -> Images:
    """The every post request handler for all needs.

    Expects a JSON object with one of the following fields: 'title', 'name'
    or 'id'. If 'title' than return existed or new base64 encoded image.
    If 'name' or 'id' than return the base64 encoded image data if exists.
    """
    if images.title:
        images_data = await ImagesRep.add_images(images)
        if isinstance(images_data, str):
            images = Images(error=images_data)
            return images
        images_data.images = [b64encode(images_data.images).decode('utf-8')]
        return images_data

    elif images.name:
        ex_images = await ImagesRep.get_images(images)
        if not ex_images:
            ex_images = Images(error='Image DOES NOT exist dear')
            return ex_images
        ex_images.images = [b64encode(ex_images.images).decode('utf-8')]
        return ex_images

    elif images.id:
        ex_images = await ImagesRep.get_images(images)
        if not ex_images:
            ex_images = Images(error='Image DOES NOT exist dear')
            return ex_images
        ex_images.images = [b64encode(ex_images.images).decode('utf-8')]
        return ex_images

    raise HTTPException(
        status_code=400,
        detail=(
            "'title' or 'name' or 'id' field are not in request BUT should be"
            )
        )
