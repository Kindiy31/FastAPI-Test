from fastapi import HTTPException, status


class PromotionAlreadyExistsForProduct(HTTPException):
    def __init__(self, product_id):
        detail: str = f"Promotion with product id: {product_id} added before"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ErrorPromotionEndDate(HTTPException):
    def __init__(self, end_date, start_date):
        detail: str = f"End date: {end_date} < Start date: {start_date}"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
