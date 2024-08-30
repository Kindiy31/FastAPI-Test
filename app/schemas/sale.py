from pydantic import BaseModel, Field
from typing import Optional


class SaleBase(BaseModel):
    product_id: int = Field(...)
    sold_quantity: int = Field(...)
    full_price: float = Field(...)
    sold_price: float = Field(...)
    discount_percentage: Optional[float] = Field(default=0)
    is_reserve: bool = Field(default=False)


class SaleCreate(BaseModel):
    product_id: int = Field(...)
    sold_quantity: int = Field(...)
