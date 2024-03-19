"""Pydantic models module."""
from pydantic import BaseModel
from typing import Optional


class ImageAdd(BaseModel):
    """The model to get from request."""
    title: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class Image(ImageAdd):
    """The model to bind with alchemy."""
    image: bytes
    byte_image_size: float
    width: int
    height: int
