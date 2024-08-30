from fastapi import APIRouter, Depends, HTTPException, Body
from app.core import get_db, Database
from app.exceptions import ReservationNotFound

from app.repositories import ReservationRepository, SaleRepository
from app.schemas import SaleCreate, SaleBase


router = APIRouter()


@router.post("/reservation/{reservation_id}/cancel_reserve")
async def cancel_reservation(
    reservation_id: int,
    db: Database = Depends(get_db)
):
    canceled_reservation = await ReservationRepository(db=db).cancel_reservation(reservation_id=reservation_id)
    if not canceled_reservation:
        raise HTTPException(status_code=404, detail="Error cancel reservation")
    return canceled_reservation


@router.post("/reservation/{reservation_id}/confirm")
async def confirm_reservation(
    reservation_id: int,
    db: Database = Depends(get_db)
):
    reservation = await ReservationRepository(db=db).get_reservation(reservation_id=reservation_id)
    if not reservation:
        raise ReservationNotFound(reservation_id=reservation_id)
    data = SaleCreate(
        product_id=reservation.product_id,
        sold_quantity=reservation.reserved_quantity
    )
    sale = await SaleRepository(db=db).add_sale(data=data, is_reserve=True, reservation_id=reservation_id)
    return sale
