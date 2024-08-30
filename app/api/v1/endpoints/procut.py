from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List

from app.models import Product, Reservation

from app.core import get_db, Database

from app.repositories import ProductRepository

from app.schemas import ProductCreate, ProductBase, ReservationBase, ProductSetPrice, ProductReservation

router = APIRouter()


@router.get("/products/", response_model=List[ProductBase])
async def get_products(
    db: Database = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    products = await ProductRepository(db=db).get_products(skip=skip, limit=limit)
    return products


@router.post("/products/", response_model=ProductBase)
async def create_product(
    product: ProductCreate,
    db: Database = Depends(get_db)
):
    new_product = await ProductRepository(db=db).add_product(product_data=product)
    return new_product


@router.patch("/products/{product_id}/price", response_model=ProductBase)
async def update_price(
    product_id: int,
    data: ProductSetPrice,
    db: Database = Depends(get_db)
):
    updated_product = await ProductRepository(db=db).update_product_price(product_id=product_id, price=data.price)
    return updated_product


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Database = Depends(get_db)
):
    success = await ProductRepository(db=db).delete_product(product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}


@router.post("/products/{product_id}/reserve", response_model=ReservationBase)
async def reserve_product(
    product_id: int,
    data: ProductReservation,
    db: Database = Depends(get_db)
):
    reserved_product = await ProductRepository(db=db).reserve_product(product_id=product_id, quantity=data.quantity)
    if not reserved_product:
        raise HTTPException(status_code=404, detail="Product not found or already reserved")
    return reserved_product
#
#
# @router.post("/products/{product_id}/cancel_reserve")
# async def cancel_reservation(
#     product_id: int,
#     db: Database = Depends(get_db)
# ):
#     canceled_reservation = await ProductRepository(db=db).cancel_reservation(product_id)
#     if not canceled_reservation:
#         raise HTTPException(status_code=404, detail="Error cancel reservation")
#     return canceled_reservation


# @router.post("/products/{product_id}/sell", response_model=Product)
# async def sell_product(
#     product_id: int,
#     db: Database = Depends(get_db)
# ):
#     sold_product = await ProductRepository(db=db).sell_product(product_id)
#     if not sold_product:
#         raise HTTPException(status_code=404, detail="Product not found or not available for sale")
#     return sold_product
#
# # Звіт про товари, що були продані
# @router.get("/products/sales_report", response_model=List[Product])
# async def sales_report(
#     filters: SaleReportFilters = Depends(),
#     db: Database = Depends(get_db)
# ):
#     report = await ProductRepository(db=db).get_sales_report(filters)
#     return report