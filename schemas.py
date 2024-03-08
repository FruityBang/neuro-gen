from pydantic import BaseModel
from typing import Optional


class ImageAdd(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class Image(ImageAdd):
    image: Optional[str]
    byte_image_size: Optional[float]
    width: Optional[int]
    height: Optional[int]
