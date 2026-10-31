from pydantic import BaseModel

class ProductBase(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductResponse(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass