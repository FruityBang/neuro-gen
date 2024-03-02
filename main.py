from fastapi import FastAPI
from router import v1_router


app = FastAPI()

app. include_router(v1_router)
