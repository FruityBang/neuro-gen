from pydantic import BaseModel
from typing import Optional


class ImageAdd(BaseModel):
    title: str
    name: Optional[str] = None


class Image(ImageAdd):
    id: int
