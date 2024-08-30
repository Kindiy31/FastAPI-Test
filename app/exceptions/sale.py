from fastapi import HTTPException, status


class SaleStockLower(HTTPException):
    def __init__(self, stock, is_reserve, product_id, quantity):
        detail: str = f"Product with id: {product_id} {'reserve' if is_reserve else ''} stock = {stock}/{quantity}"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
