from fastapi import APIRouter, Depends

from app.core import get_db, Database

from app.repositories import CategoryRepository

from app.schemas import CategoryCreate, CategoryBase

router = APIRouter()


@router.post("/category/", response_model=CategoryBase)
async def add_category(
    data: CategoryCreate,
    db: Database = Depends(get_db)
):
    category = await CategoryRepository(db=db).add_category(data=data)
    return category
