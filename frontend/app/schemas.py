from datetime import datetime
from typing import List, Union
from pydantic import BaseModel


#################### ITEM ####################


# Common values shared by each Item
class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None
    price: float
    old_price: Union[float, None] = None
    image: str
    location: str
    condition: str
    owner_id: int
    category_id: int
    product_id: int


# Values needed when creating a new Item
class ItemCreate(ItemBase):
    pass


# Values needed when reading an Item
class Item(ItemBase):
    id: int
    date: datetime
    is_available: bool

    class Config:
        orm_mode = True


#################### USER ####################


# Common values shared by each User
class UserBase(BaseModel):
    username: str
    name: str
    email: str
    avatar: Union[str, None] = None
    phone: int
    location: str


# Values needed when creating a new User
class UserCreate(UserBase):
    token: str


# Values needed when reading an User
class User(UserBase):
    id: int
    rating: float
    total_sales: int
    total_purchases: int
    total_reviews: int
    registration: datetime
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
