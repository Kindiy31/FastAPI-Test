from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    reserved_stock = Column(Integer, default=0)
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'), nullable=False)
    subcategory = relationship('SubCategory', back_populates='products')
