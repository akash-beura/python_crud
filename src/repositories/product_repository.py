from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import get_db
from src.entities.product import ProductEntity
from src.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self) -> list[ProductEntity]:
        return list(self.db.scalars(select(ProductEntity)).all())

    def get_by_id(self, product_id: int) -> ProductEntity | None:
        return self.db.get(ProductEntity, product_id)

    def create(self, new_product: ProductCreate) -> ProductEntity:
        entity = ProductEntity(**new_product.model_dump())
        try:
            self.db.add(entity)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise
        self.db.refresh(entity)
        return entity

    def update(self, updated_product: ProductUpdate) -> ProductEntity | None:
        entity = self.db.get(ProductEntity, updated_product.id)
        if entity is None:
            return None
        entity.name = updated_product.name
        entity.description = updated_product.description
        entity.price = updated_product.price
        entity.quantity = updated_product.quantity
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, product_id: int) -> bool:
        entity = self.db.get(ProductEntity, product_id)
        if entity is None:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True
