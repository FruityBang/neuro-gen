from fastapi import APIRouter

v1_router = APIRouter(prefix='/v1')

@v1_router.post('/')

