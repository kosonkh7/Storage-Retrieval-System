from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
from app.core.base import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)

    # inventories = relationship("Inventory", back_populates="product")