from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.core import Base


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    status = Column(Integer, default=0)
    reserved_quantity = Column(Integer, nullable=False)
    reservation_date = Column(DateTime, default=func.now())
    product = relationship('Product')
