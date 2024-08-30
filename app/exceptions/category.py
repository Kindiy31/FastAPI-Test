from fastapi import HTTPException, status


class CategoryNotFound(HTTPException):
    def __init__(self, category_id):
        detail: str = f"Category with id: {category_id} not founded"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
