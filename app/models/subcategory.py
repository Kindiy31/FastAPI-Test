from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core import Base


class SubCategory(Base):
    __tablename__ = 'subcategories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', back_populates='subcategories')
    products = relationship('Product', back_populates='subcategory')
