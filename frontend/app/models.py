from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, Boolean, String, Float, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    token = Column(String(500), index=True)  # unique=True / primary_key ???
    username = Column(String(500), unique=True, index=True)
    name = Column(String(500))
    email = Column(String(500), unique=True, index=True)
    avatar = Column(String(500), default=None)
    rating = Column(Float, default=0.0)
    total_sales = Column(Integer, default=0)
    total_purchases = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    phone = Column(Integer, unique=True)
    registration = Column(DateTime, default=datetime.now)
    location = Column(String(500))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(500), index=True)
    date = Column(DateTime, default=datetime.now)
    description = Column(String(500))
    price = Column(Float)
    old_price = Column(Float, default=None)  # optional
    image = Column(String(500))
    location = Column(String(500))
    condition = Column(String(500))
    is_available = Column(Boolean, default=True)
    owner_id = Column(String(500), ForeignKey("users.id"))
    # ForeignKey("categories.id")) external database/table
    category_id = Column(Integer)
    # ForeignKey("products.id")) external database/table
    product_id = Column(Integer)

    owner = relationship("User", back_populates="items")
