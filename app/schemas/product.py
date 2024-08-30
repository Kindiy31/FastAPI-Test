from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)
    reserved_stock: Optional[int] = Field(default=0)
    subcategory_id: int = Field(...)


class ProductSetPrice(BaseModel):
    price: float


class ProductReservation(BaseModel):
    quantity: int


class ProductCreate(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the product")
    price: int = Field(..., ge=0, description="The price of the product in cents")
    stock: int = Field(..., ge=0, description="The quantity available for sale")
    subcategory_id: int = Field(..., ge=0, description="The id for subcategory")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Lenovo T450",
                "price": 150,
                "stock": 10,
                "subcategory_id": 1
            }
        }
