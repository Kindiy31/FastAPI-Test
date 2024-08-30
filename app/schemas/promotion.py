from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union


class PromotionCreate(BaseModel):
    discount_percentage: float = Field(..., ge=0, le=100)
    start_date: datetime = Field(default=datetime.now())
    end_date: datetime = Field(default=None)
    product_id: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "discount_percentage": 20.0,
                "start_date": "2024-09-01T12:00:00",
                "end_date": "2024-10-01T12:00:00",
                "product_id": 1
            }
        }


class PromotionBase(BaseModel):
    status: int = Field(...)
    discount_percentage: float = Field(...)
    start_date: datetime = Field(...)
    end_date: Union[datetime, None] = Field(default=None)
    product_id: int = Field(...)
