from app.models import Promotion
from app.core import Database

from sqlalchemy import func, or_

from app.schemas import PromotionCreate

from app.exceptions import ProductNotFound, PromotionAlreadyExistsForProduct, ErrorPromotionEndDate

from app.repositories import ProductRepository


class PromotionRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_promotion(self, promotion_id: int) -> Promotion:
        promotion = await self.db.get_data(
            table=Promotion,
            where=[Promotion.id == promotion_id],
            fetchall=False
        )
        return promotion

    async def get_promotion_for_product(self, product_id: int) -> Promotion:
        where = [
            Promotion.product_id == product_id,
            Promotion.status == 1,
            Promotion.start_date < func.now(),
            or_(
                Promotion.end_date > func.now(),
                Promotion.end_date.is_(None)
            )
        ]
        promotion = await self.db.get_data(
            table=Promotion,
            where=where,
            fetchall=False
        )
        return promotion

    async def add_promotion(self, data: PromotionCreate) -> Promotion:
        product = await ProductRepository(db=self.db).get_product(product_id=data.product_id)
        if not product:
            raise ProductNotFound(product_id=data.product_id)
        exist_promotion = await self.get_promotion_for_product(product_id=data.product_id)
        if exist_promotion:
            raise PromotionAlreadyExistsForProduct(product_id=data.product_id)
        if data.end_date:
            if data.end_date < data.start_date:
                raise ErrorPromotionEndDate(end_date=data.end_date, start_date=data.start_date)
        promotion = Promotion(
            discount_percentage=data.discount_percentage,
            start_date=data.start_date,
            end_date=data.end_date,
            product_id=data.product_id
        )
        await self.db.add(model=promotion)
        return promotion
