from fastapi import APIRouter, Depends

from app.core import get_db, Database

from app.repositories import PromotionRepository

from app.schemas import PromotionCreate, PromotionBase

router = APIRouter()


@router.post("/promotion/", response_model=PromotionBase)
async def add_promotion(
    data: PromotionCreate,
    db: Database = Depends(get_db)
):
    promotion = await PromotionRepository(db=db).add_promotion(data=data)
    return promotion
