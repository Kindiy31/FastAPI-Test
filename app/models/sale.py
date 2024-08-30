from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Float, Boolean
from sqlalchemy.orm import relationship

from app.core import Base


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    sold_quantity = Column(Integer, nullable=False)
    full_price = Column(Float)
    sold_price = Column(Float)
    discount_percentage = Column(Float, default=0)
    is_reserve = Column(Boolean, default=False)
    sale_date = Column(DateTime, default=func.now())
    product = relationship('Product')
