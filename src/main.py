from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from src.api.middleware.request_id import add_request_id
from src.api.routes import product
from src.core.config import settings

version = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting....")
    async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
        app.state.http_client = client
        print("Http Client Initialised..")
        yield
    print("App is shutting down...")


app = FastAPI(version=version, lifespan=lifespan)
app.middleware("http")(add_request_id)
app.include_router(product.router, prefix=f"/api/{version}")
