"""Suddenly the main part."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from db import create_tables, delete_tables
from V1_api.v1_router import v1_router
from V2_api.v2_router import v2_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Developing moment."""
    await delete_tables()
    print('очистка')
    await create_tables()
    print('готова дб')
    yield
    print('stop')


app = FastAPI()
app.include_router(v1_router)
app.include_router(v2_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
