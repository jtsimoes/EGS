from http.client import HTTPException
import json
import uuid
from fastapi import FastAPI, Query
from uuid import UUID
from pydantic import BaseModel, Field
import csv


app = FastAPI(title="Inventory API", version="1.0.0")

# dummy data
categories = []
products = []

class Category(BaseModel):
    name: str = Field(..., description="The name of the category")
    id: UUID = Field(..., description="The ID of the category")
    image: str = Field("", description="The image url of the category")

class NewCategory(BaseModel):
    name: str = Field(..., description="The name of the new category")
    image: str = Field("", description="The image url of the new category")


class Product(BaseModel):
    name: str = Field(..., description="The name of the product")
    description: str = Field("", description="The description of the product")
    id: UUID = Field(..., description="The ID of the product")
    category_id: UUID = Field(..., description="The ID of the category that the product belongs to")
    image: str = Field("", description="The image url of the product")


class NewProduct(BaseModel):
    name: str = Field(..., description="The name of the new product")
    description: str = Field("", description="The description of the new product")
    category_id: UUID = Field(..., description="The ID of the category that the new product belongs to")
    image: str = Field("", description="The image url of the new product")



@app.on_event("startup")
async def startup_event():
    with open('categories.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            category_id = row[0]
            name = row[1]
            image = row[2]
            category = Category(id=category_id, name=name, image=image)
            categories.append(category)
            print(category)

    with open('products.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            product_id = row[0]
            name = row[1]
            description = row[2]
            category_id = row[3]
            image = row[4]
            product = Product(id=product_id, name=name, description=description, category_id=category_id, image=image)
            products.append(product)
            print(product)


@app.get("/")
async def root():
    return {"message": "Server is UP"}


@app.get("/v1/categories",tags=["categories"])
async def get_categories(limit: int = Query(50, ge=1, le=50), offset: int = Query(0, ge=0)):
    return categories[offset:offset+limit]


@app.post("/v1/categories", response_model=Category, status_code=201,tags=["categories"])
async def create_category(new_category: NewCategory):
    category_id = (uuid.uuid4())
    category = Category(id=category_id, name=new_category.name, image=new_category.image)
    categories.append(category)
    print(category)
    with open('categories.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([category_id, new_category.name, new_category.image])
    return category


@app.get("/v1/categories/{categoryId}", response_model=Category,tags=["categories"])
async def get_category(categoryId: UUID):
    for category in categories:
        if category.id == categoryId:
            return category
    raise HTTPException(status_code=404, detail="Category not found")


@app.delete("/v1/categories/{categoryId}", status_code=204,tags=["categories"])
async def delete_category(categoryId: UUID):
    for i, category in enumerate(categories):
        if category.id == categoryId:
            del categories[i]
            return
    raise HTTPException(status_code=404, detail="Category not found")


@app.put("/v1/categories/{categoryId}", response_model=Category,tags=["categories"])
async def update_category(categoryId: UUID, updated_category: Category):
    for i, c in enumerate(categories):
        if c.id == categoryId:
            categories[i] = update_category
            return update_category
        
    raise HTTPException(status_code=404, detail="Category not found")
            

@app.get("/v1/products",tags=["products"])
async def get_products(categoryId: UUID = None, limit: int = Query(50, ge=1, le=50), offset: int = Query(0, ge=0),tags=["products"]):
    if categoryId:
        filtered_products = []
        for product in products:
            if product.category_id == categoryId:
                filtered_products.append(product)
        return filtered_products[offset:offset+limit]
    return products[offset:offset+limit]


@app.post("/v1/products", response_model=Product, status_code=201,tags=["products"])
async def create_product(new_product: NewProduct):
    product_id = (uuid.uuid4())
    product = Product(id=product_id, name=new_product.name, description=new_product.description, category_id=new_product.category_id, image= new_product.image)
    products.append(product)
    print(product)
    with open('products.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([product_id, new_product.name, new_product.description, new_product.category_id, new_product.image])
    return product


@app.get("/v1/products/{productId}", response_model=Product,tags=["products"])
async def get_product(productId: UUID):
    for product in products:
        if product.id == productId:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/v1/products/{productId}", status_code=204,tags=["products"])
async def delete_product(productId: UUID):
    for i, product in enumerate(products):
        if product.id == productId:
            del products[i]
            return
    raise HTTPException(status_code=404, detail="Product not found")

