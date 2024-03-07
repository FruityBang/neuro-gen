from pydantic import BaseModel
from typing import Optional


class ImageAdd(BaseModel):
    title: str


class Image(ImageAdd):
    id: int
    name: str
    image: Optional[str]
    byte_image_size: Optional[float]
    width: Optional[int]
    height: Optional[int]
