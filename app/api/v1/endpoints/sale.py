from fastapi import APIRouter, Depends
from app.core import get_db, Database

from app.repositories import SaleRepository

from app.schemas import SaleCreate, SaleBase


router = APIRouter()


@router.post("/sale/", response_model=SaleBase)
async def sale_product(
    data: SaleCreate,
    db: Database = Depends(get_db)
):
    sale = await SaleRepository(db=db).add_sale(data=data, is_reserve=False)
    return sale
