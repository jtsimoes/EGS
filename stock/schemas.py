from uuid import UUID
from pydantic import BaseModel, Field

class Category(BaseModel):
    name: str = Field(..., description="The name of the category")
    id: int = Field(..., description="The ID of the category")
    image: str = Field("", description="The image url of the category")
    class Config:
        orm_mode = True


class NewCategory(BaseModel):
    name: str = Field(..., description="The name of the new category")
    image: str = Field("", description="The image url of the new category")


class SubCategory(BaseModel):
    name: str = Field(..., description="The name of the subcategory")
    category_id: int = Field(..., description="The ID of the category that the subcategory belongs to")
    id: int = Field(..., description="The ID of the subcategory")
    image: str = Field("", description="The image url of the subcategory")
    class Config:
        orm_mode = True


class NewSubCategory(BaseModel):
    name: str = Field(..., description="The name of the new subcategory")
    category_id: int = Field(..., description="The ID of the category that the new subcategory belongs to")
    image: str = Field("", description="The image url of the new subcategory")


class Product(BaseModel):
    name: str = Field(..., description="The name of the product")
    description: str = Field("", description="The description of the product")
    id: int = Field(..., description="The ID of the product")
    category_id: int = Field(...,description="The ID of the category that the product belongs to")
    subcategory_id: int = Field(..., description="The ID of the subcategory that the product belongs to")
    image: str = Field("", description="The image url of the product")
    class Config:
        orm_mode = True


class NewProduct(BaseModel):
    name: str = Field(..., description="The name of the new product")
    description: str = Field("", description="The description of the new product")
    category_id: int = Field(..., description="The ID of the category that the new product belongs to")
    subcategory_id: int = Field(..., description="The ID of the subcategory that the product belongs to")
    image: str = Field("", description="The image url of the new product")
    