from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from models import ProductCreate, ProductUpdate, ProductResponse, ProductBase
from random import randint
from database import get_db, Base, engine, SessionLocal
from database_models import ProductEntity
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    product_entities = db.query(ProductEntity).all()
    product_response = []
    for product in product_entities:
        product_response.append(ProductResponse.model_validate(product, from_attributes=True))
    return product_response

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product_entity = db.query(ProductEntity).filter(ProductEntity.id == id).first()
    if product_entity:
        return ProductResponse.model_validate(product_entity, from_attributes=True)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@app.post("/product")
def add_product(new_product: ProductCreate, db: Session = Depends(get_db)):
    try:
        entity = ProductEntity(**new_product.model_dump())
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return ProductResponse.model_validate(entity, from_attributes=True)
    except IntegrityError as ex:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product conflicts with existing data")

@app.put("/product")
def update_product(updated_product: ProductUpdate, db: Session = Depends(get_db)):
    entity = db.query(ProductEntity).filter(ProductEntity.id == updated_product.id).first()
    if entity:
        entity.name = updated_product.name
        entity.description = updated_product.description
        entity.price = updated_product.price
        entity.quantity = updated_product.quantity
        db.commit()
        return "Product updated.."
    else:
        return "No Product Found.."



@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    entity = db.query(ProductEntity).filter(ProductEntity.id == id).first()
    if not entity:
        return "No product with id found.."
    else:
        db.delete(entity)
        db.commit()
        return f"Product with ID = {id} deleted..."
