from app.models import SubCategory
from app.core import Database

from app.schemas import SubCategoryCreate

from app.repositories import CategoryRepository

from app.exceptions import CategoryNotFound


class SubCategoryRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_sub_category(self, sub_category_id) -> SubCategory:
        sub_category = await self.db.get_data(
            table=SubCategory,
            where=[SubCategory.id == sub_category_id],
            fetchall=False
        )
        return sub_category

    async def add_sub_category(self, data: SubCategoryCreate) -> SubCategory:
        category = await CategoryRepository(db=self.db).get_category(category_id=data.category_id)
        if not category:
            raise CategoryNotFound(category_id=data.category_id)
        sub_category = SubCategory(
            name=data.name,
            category_id=data.category_id
        )
        await self.db.add(model=sub_category)
        return sub_category
