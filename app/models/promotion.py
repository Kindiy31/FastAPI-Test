from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship

from app.core import Base


class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, index=True, default=1)
    discount_percentage = Column(Float, nullable=False)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product')
