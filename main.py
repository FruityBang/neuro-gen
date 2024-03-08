from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from db import create_tables, delete_tables
from router import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('очистка')
    await create_tables()
    print('готова дб')
    yield
    print('stop')


app = FastAPI()
app.include_router(v1_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
