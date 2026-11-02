from src.api.middleware.request_id import add_request_id
from src.api.routes import product
from fastapi import FastAPI

from src.core.config import Settings


version = "v1"
app = FastAPI(version=version)
settings = Settings()
print(settings)
app.middleware("http")(add_request_id)
app.include_router(product.router, prefix=f"/api/{version}")



