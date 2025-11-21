from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # İlişki: Bir kategorinin birden çok ürünü olabilir
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
    
    # İlişki: Hangi kategoriye ait?
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")