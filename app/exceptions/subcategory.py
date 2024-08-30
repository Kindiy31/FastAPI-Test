from fastapi import HTTPException, status


class SubCategoryNotFound(HTTPException):
    def __init__(self, sub_category_id):
        detail: str = f"Sub category with id: {sub_category_id} not founded"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
