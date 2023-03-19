from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, Boolean, String, Float, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    token = Column(String, index=True)  # unique=True / primary_key ???
    username = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    avatar = Column(String, default=None)
    rating = Column(Float, default=0.0)
    total_sales = Column(Integer, default=0)
    total_purchases = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    phone = Column(Integer, unique=True)
    registration = Column(DateTime, default=datetime.now)
    location = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    date = Column(DateTime, default=datetime.now)
    description = Column(String)
    price = Column(Float)
    old_price = Column(Float, default=None)  # optional
    image = Column(String)
    location = Column(String)
    condition = Column(String)
    is_available = Column(Boolean, default=True)
    owner_id = Column(String, ForeignKey("users.id"))
    # ForeignKey("categories.id")) external database/table
    category_id = Column(Integer)
    # ForeignKey("products.id")) external database/table
    product_id = Column(Integer)

    owner = relationship("User", back_populates="items")
