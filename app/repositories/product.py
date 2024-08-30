from sqlalchemy import select
from app.models import Product, Reservation
from app.core import Database

from app.schemas import ProductCreate, ReservationCreate, SaleCreate

from app.exceptions import ProductNotFound, ProductStockTooLowException, ReservationNotFound, SubCategoryNotFound, \
    SaleStockLower


class ProductRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_product(self, product_id) -> Product:
        product = await self.db.get_data(
            table=Product,
            where=[Product.id == product_id],
            fetchall=False
        )
        return product

    async def get_products(self, skip: int = 0, limit: int = 10):
        where = [Product.stock > 0]
        order_by = Product.name.asc()
        return await self.db.get_data(table=Product, where=where, limit=limit, offset=skip, order_by=order_by)

    async def validate_product(self, product_id) -> Product:
        product = await self.get_product(product_id=product_id)
        if not product:
            raise ProductNotFound(product_id=product_id)
        return product

    async def add_product(self, product_data: ProductCreate) -> Product:
        from app.repositories import SubCategoryRepository
        subcategory = await (SubCategoryRepository(db=self.db)
                             .get_sub_category(sub_category_id=product_data.subcategory_id))
        if not subcategory:
            raise SubCategoryNotFound(sub_category_id=product_data.subcategory_id)
        product = Product(
            name=product_data.name,
            stock=product_data.stock,
            price=product_data.price,
            subcategory_id=product_data.subcategory_id
        )
        await self.db.add(model=product)
        return product

    async def update_product_price(self, product_id: int, price: float) -> Product:
        product = await self.validate_product(product_id=product_id)
        where = [Product.id == product_id]
        product.price = price
        data = {
            Product.price: price
        }
        await self.db.update(table=Product, data=data, where=where)
        return product

    async def delete_product(self, product_id: int):
        where = [Product.id == product_id]
        return await self.db.delete(table=Product, where=where)

    async def reserve_product(self, product_id: int, quantity: int) -> Reservation:
        from app.repositories import ReservationRepository
        product = await self.validate_product(product_id=product_id)
        if product.stock < quantity:
            raise ProductStockTooLowException()
        where = [Product.id == product_id]
        update_data = {
            Product.stock: Product.stock - quantity,
            Product.reserved_stock: Product.reserved_stock + quantity
        }
        reservation_create = ReservationCreate(
            product_id=product_id,
            reserved_quantity=quantity
        )
        await self.db.update(table=Product, data=update_data, where=where)
        reservation = await ReservationRepository(db=self.db).create_reservation(data=reservation_create)
        return reservation

    async def cancel_reservation(self, reservation: Reservation):
        product = await self.validate_product(product_id=reservation.product_id)
        where = [Product.id == product.id]
        update_data = {
            Product.stock: Product.stock + reservation.reserved_quantity,
            Product.reserved_stock: Product.reserved_stock - reservation.reserved_quantity
        }
        await self.db.update(table=Product, data=update_data, where=where)
        return True

    async def sell_product(self, product: Product, data: SaleCreate, is_reserve):
        if is_reserve:
            column = Product.reserved_stock
            value = product.reserved_stock
        else:
            column = Product.stock
            value = product.stock
        if value < data.sold_quantity:
            raise SaleStockLower(stock=value, product_id=data.product_id,
                                 quantity=data.sold_quantity, is_reserve=is_reserve)
        where = [Product.id == product.id]
        data = {
            column: column - data.sold_quantity
        }
        await self.db.update(
            table=Product,
            data=data,
            where=where
        )
        return True

    async def get_sold_products_report(self, filters: dict = None):
        # Implement the report generation logic here, applying filters as needed
        where = []
        if filters:
            for key, value in filters.items():
                where.append(getattr(Product, key) == value)
        return await self.db.get_data(Product, where=where, fetchall=True)

