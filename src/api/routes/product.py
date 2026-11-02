from src.repositories.product_repository import ProductRepository
from fastapi import Depends, HTTPException, APIRouter, status
from src.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    tags=["Products"],
    prefix="/products"
)

@router.get("/all")
def get_products(repo: ProductRepository = Depends()):
    product_entities = repo.get_all()
    product_response = []
    for product in product_entities:
        product_response.append(ProductResponse.model_validate(product, from_attributes=True))
    return product_response

@router.get("/{id}")
def get_product_by_id(id: int, repo: ProductRepository = Depends()):
    product_entity = repo.get_by_id(id)
    if product_entity:
        return ProductResponse.model_validate(product_entity, from_attributes=True)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@router.post("/")
def add_product(new_product: ProductCreate, repo: ProductRepository = Depends()):
    try:
        entity = repo.create(new_product)
        return ProductResponse.model_validate(entity, from_attributes=True)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product conflicts with existing data")

@router.put("/")
def update_product(updated_product: ProductUpdate, repo: ProductRepository = Depends()):
    entity = repo.update(updated_product)
    if entity:
        return "Product updated.."
    else:
        return "No Product Found.."

@router.delete("/{id}")
def delete_product(id: int, repo: ProductRepository = Depends()):
    if not repo.delete(id):
        return "No product with id found.."
    else:
        return f"Product with ID = {id} deleted..."