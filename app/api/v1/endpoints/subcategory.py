from fastapi import APIRouter, Depends

from app.core import get_db, Database

from app.repositories import SubCategoryRepository

from app.schemas import SubCategoryCreate, SubCategoryBase

router = APIRouter()


@router.post("/subcategory/", response_model=SubCategoryBase)
async def add_sub_category(
    data: SubCategoryCreate,
    db: Database = Depends(get_db)
):
    category = await SubCategoryRepository(db=db).add_sub_category(data=data)
    return category
