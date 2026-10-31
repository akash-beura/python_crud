from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, CheckConstraint
from decimal import Decimal

from src.database.base import Base

class ProductEntity(Base):
    __tablename__ = "product"
    __table_args__ = (CheckConstraint("quantity >= 0", name="ck_product_quantity_nonnegative"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int]
