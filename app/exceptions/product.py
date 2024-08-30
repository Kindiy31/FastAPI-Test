from fastapi import HTTPException, status


class ProductNotFound(HTTPException):
    def __init__(self, product_id):
        detail: str = f"Product with id: {product_id} not founded"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ProductStockTooLowException(HTTPException):
    def __init__(self):
        detail: str = "Product stock is too low"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
