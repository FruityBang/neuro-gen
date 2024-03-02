from pydantic import BaseModel


class NewImage(BaseModel):
    title: str
    name: str
