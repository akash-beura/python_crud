from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError

from src.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from src.database import Base, engine
from src.repositories.product_repository import ProductRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/products")
def get_products(repo: ProductRepository = Depends()):
    product_entities = repo.get_all()
    product_response = []
    for product in product_entities:
        product_response.append(ProductResponse.model_validate(product, from_attributes=True))
    return product_response

@app.get("/products/{id}")
def get_product_by_id(id: int, repo: ProductRepository = Depends()):
    product_entity = repo.get_by_id(id)
    if product_entity:
        return ProductResponse.model_validate(product_entity, from_attributes=True)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@app.post("/product")
def add_product(new_product: ProductCreate, repo: ProductRepository = Depends()):
    try:
        entity = repo.create(new_product)
        return ProductResponse.model_validate(entity, from_attributes=True)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product conflicts with existing data")

@app.put("/product")
def update_product(updated_product: ProductUpdate, repo: ProductRepository = Depends()):
    entity = repo.update(updated_product)
    if entity:
        return "Product updated.."
    else:
        return "No Product Found.."

@app.delete("/product/{id}")
def delete_product(id: int, repo: ProductRepository = Depends()):
    if not repo.delete(id):
        return "No product with id found.."
    else:
        return f"Product with ID = {id} deleted..."
