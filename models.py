from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class SendImage(TunedModel):
    title: str
    name: str


class CreateImage(BaseModel):
    title: str
