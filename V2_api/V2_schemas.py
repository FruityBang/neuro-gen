"""Pydantic models module V2."""
from pydantic import BaseModel
from typing import Optional


class ImagesAdd(BaseModel):
    """The model to get from request."""
    title: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class Images(ImagesAdd):
    """The model to bind with alchemy."""
    images: Optional[list[str]] = None
    byte_image_size_kB: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    error: Optional[str] = None
