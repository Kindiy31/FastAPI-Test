from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the category")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "laptop"
            }
        }


class CategoryBase(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
