from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReservationCreate(BaseModel):
    product_id: int = Field(...)
    reserved_quantity: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "1",
                "reserved_quantity": 3
            }
        }


class ReservationBase(BaseModel):
    id: int = Field(...)
    product_id: int = Field(...)
    status: int = Field(default=0)
    reserved_quantity: int = Field(...)

