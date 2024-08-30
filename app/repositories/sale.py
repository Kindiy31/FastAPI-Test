from app.exceptions import ReservationNotFound
from app.models import Sale
from app.core import Database

from app.schemas import SaleCreate

from typing import List


class SaleRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_sales(self) -> List[Sale]:
        sales = await self.db.get_data(
            table=Sale
        )
        return sales

    async def add_sale(self, data: SaleCreate, is_reserve, reservation_id=None) -> Sale:
        from app.repositories import ProductRepository
        from app.repositories import PromotionRepository
        product_repository = ProductRepository(db=self.db)
        promotion_repository = PromotionRepository(db=self.db)
        product = await product_repository.validate_product(product_id=data.product_id)
        if is_reserve and reservation_id:
            from app.repositories import ReservationRepository
            reservation_repository = ReservationRepository(db=self.db)
            await reservation_repository.confirm_reservation(reservation_id=reservation_id)
        await product_repository.sell_product(product=product, data=data, is_reserve=is_reserve)
        promotion = await promotion_repository.get_promotion_for_product(product_id=data.product_id)
        if promotion:
            discount = promotion.discount_percentage
            price_for_product = round(float(eval(f"{product.price} - ({product.price} * {discount} / 100)")), 2)
        else:
            discount = 0
            price_for_product = product.price
        full_price = round(float(eval(f"{product.price} * {data.sold_quantity}")), 2)
        sold_price = round(float(eval(f"{price_for_product} * {data.sold_quantity} * {discount} / 100")), 2)
        sale = Sale(
            product_id=data.product_id,
            sold_quantity=data.sold_quantity,
            full_price=full_price,
            sold_price=sold_price,
            discount_percentage=discount,
            is_reserve=is_reserve
        )
        await self.db.add(sale)
        return sale
