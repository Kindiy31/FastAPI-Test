from app.models import Category
from app.core import Database

from app.schemas import CategoryCreate


class CategoryRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_category(self, category_id) -> Category:
        category = await self.db.get_data(
            table=Category,
            where=[Category.id == category_id],
            fetchall=False
        )
        return category

    async def add_category(self, data: CategoryCreate) -> Category:
        category = Category(
            name=data.name
        )
        await self.db.add(model=category)
        return category
