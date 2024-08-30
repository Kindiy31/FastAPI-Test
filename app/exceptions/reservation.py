from fastapi import HTTPException, status


class ReservationNotFound(HTTPException):
    def __init__(self, reservation_id):
        detail: str = f"Reservation with id: {reservation_id} not founded"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ReservationAlreadyCanceled(HTTPException):
    def __init__(self, reservation_id):
        detail: str = f"Reservation with id: {reservation_id} already canceled"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ReservationAlreadyConfirmed(HTTPException):
    def __init__(self, reservation_id):
        detail: str = f"Reservation with id: {reservation_id} already confirmed"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
