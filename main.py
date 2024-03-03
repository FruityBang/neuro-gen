from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel
from typing import Annotated


app = FastAPI()


class ImageAdd(BaseModel):
    title: str


@app.post('/v1/image')
def get_image(image: Annotated[ImageAdd, Depends()]):
    return {'data': image}


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
