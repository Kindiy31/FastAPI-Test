from app.exceptions import ReservationNotFound, ReservationAlreadyCanceled, ReservationAlreadyConfirmed
from app.models import Reservation
from app.core import Database

from app.schemas import ReservationCreate, SaleCreate


class ReservationRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_reservation(self, reservation_id) -> Reservation:
        reservation = await self.db.get_data(
            table=Reservation,
            where=[Reservation.id == reservation_id],
            fetchall=False
        )
        return reservation

    async def create_reservation(self, data: ReservationCreate) -> Reservation:
        reservation = Reservation(
            product_id=data.product_id,
            reserved_quantity=data.reserved_quantity
        )
        await self.db.add(model=reservation)
        return reservation

    async def cancel_reservation(self, reservation_id: int) -> Reservation:
        from app.repositories import ProductRepository
        reservation = await self.get_reservation(reservation_id=reservation_id)
        if not reservation:
            raise ReservationNotFound(reservation_id=reservation_id)
        if reservation.status == -1:
            raise ReservationAlreadyCanceled(reservation_id=reservation_id)
        if reservation.status == 1:
            raise ReservationAlreadyConfirmed(reservation_id=reservation_id)
        reservation.status = -1
        data = {
            Reservation.status: reservation.status
        }
        where = [Reservation.id == reservation_id]
        await self.db.update(table=Reservation, data=data, where=where)
        await ProductRepository(db=self.db).cancel_reservation(reservation=reservation)
        return reservation

    async def confirm_reservation(self, reservation_id: int):
        reservation = await self.get_reservation(reservation_id=reservation_id)
        if not reservation:
            raise ReservationNotFound(reservation_id=reservation_id)
        if reservation.status == 1:
            raise ReservationAlreadyConfirmed(reservation_id=reservation_id)
        if reservation.status == -1:
            raise ReservationAlreadyCanceled(reservation_id=reservation_id)
        reservation.status = 1
        data = {
            Reservation.status: reservation.status
        }
        where = [Reservation.id == reservation_id]
        await self.db.update(table=Reservation, data=data, where=where)
        return True
