from pydantic import BaseModel, Field


class SubCategoryCreate(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the sub category")
    category_id: int = Field(..., description="category id")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Lenovo",
                "category_id": 1
            }
        }


class SubCategoryBase(BaseModel):
    id: int
    name: str
    category_id: int
