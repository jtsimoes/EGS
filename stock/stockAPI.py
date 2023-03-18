import os
from fastapi.exceptions import HTTPException
import json
import uuid
from fastapi import FastAPI, Query, Request
from uuid import UUID
from pydantic import BaseModel, Field
import csv


app = FastAPI(title="Inventory API", version="1.0.0")

# dummy data
categories = []
products = []
subcategories = []


class Category(BaseModel):
    name: str = Field(..., description="The name of the category")
    id: UUID = Field(..., description="The ID of the category")
    image: str = Field("", description="The image url of the category")


class NewCategory(BaseModel):
    name: str = Field(..., description="The name of the new category")
    image: str = Field("", description="The image url of the new category")


class SubCategory(BaseModel):
    name: str = Field(..., description="The name of the subcategory")
    category_id: UUID = Field(
        ..., description="The ID of the category that the subcategory belongs to")
    id: UUID = Field(..., description="The ID of the subcategory")
    image: str = Field("", description="The image url of the subcategory")


class NewSubCategory(BaseModel):
    name: str = Field(..., description="The name of the new subcategory")
    category_id: UUID = Field(
        ..., description="The ID of the category that the new subcategory belongs to")
    image: str = Field("", description="The image url of the new subcategory")


class Product(BaseModel):
    name: str = Field(..., description="The name of the product")
    description: str = Field("", description="The description of the product")
    id: UUID = Field(..., description="The ID of the product")
    category_id: UUID = Field(...,
                              description="The ID of the category that the product belongs to")
    subcategory_id: UUID = Field(
        ..., description="The ID of the subcategory that the product belongs to")
    image: str = Field("", description="The image url of the product")


class NewProduct(BaseModel):
    name: str = Field(..., description="The name of the new product")
    description: str = Field(
        "", description="The description of the new product")
    category_id: UUID = Field(
        ..., description="The ID of the category that the new product belongs to")
    subcategory_id: UUID = Field(
        ..., description="The ID of the subcategory that the product belongs to")
    image: str = Field("", description="The image url of the new product")


@app.on_event("startup")
async def startup_event():
    if os.stat("categories.csv").st_size != 0:
        with open('categories.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                category_id = row[0]
                name = row[1]
                image = row[2]
                category = Category(id=category_id, name=name, image=image)
                categories.append(category)
                print(category)

    if os.stat("products.csv").st_size != 0:
        with open('products.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                product_id = row[0]
                name = row[1]
                description = row[2]
                category_id = row[3]
                subcategory_id = row[4]
                image = row[5]
                product = Product(id=product_id, name=name,
                                  description=description, category_id=category_id, subcategory_id=subcategory_id, image=image)
                products.append(product)
                print(product)

    if os.stat("subcategories.csv").st_size != 0:
        with open('subcategories.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                subcategory_id = row[0]
                category_id = row[1]
                name = row[2]
                image = row[3]
                subcategory = SubCategory(id=subcategory_id, name=name,
                                          category_id=category_id, image=image)
                subcategories.append(subcategory)
                print(subcategory)


@app.get("/")
async def root():
    return {"message": "Server is UP"}

# Categories


@app.get("/v1/categories", status_code=200, tags=["categories"])
async def get_categories(limit: int = Query(50, ge=1, le=50), offset: int = Query(0, ge=0)):
    if len(categories) < offset:
        raise HTTPException(status_code=404, detail="Offset is greater than the number of categories")
    return categories[offset:offset+limit]


@app.post("/v1/categories", response_model=Category, status_code=201, tags=["categories"])
async def create_category(new_category: NewCategory):
    category_id = (uuid.uuid4())
    category = Category(
        id=category_id, name=new_category.name, image=new_category.image)
    categories.append(category)
    print(category)
    with open('categories.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([category_id, new_category.name, new_category.image])

    return category


@app.get("/v1/categories/{categoryId}", status_code=200, response_model=Category, tags=["categories"])
async def get_category(categoryId: UUID):
    for category in categories:
        if category.id == categoryId:
            return category
    raise HTTPException(status_code=404, detail="Category not found")


@app.delete("/v1/categories/{categoryId}", status_code=204, tags=["categories"])
async def delete_category(categoryId: UUID):
    for i, category in enumerate(categories):
        if category.id == categoryId:
            del categories[i]
            return
    raise HTTPException(status_code=404, detail="Category not found")


@app.put("/v1/categories/{categoryId}", status_code=202, response_model=Category, tags=["categories"])
async def update_category(categoryId: UUID, updated_category: Category):
    for i, c in enumerate(categories):
        if c.id == categoryId:
            categories[i] = update_category
            return update_category
    raise HTTPException(status_code=404, detail="Category not found")

# Subcategories


@app.get("/v1/subcategories", status_code=200, tags=["subcategories"])
async def get_subcategories(categoryId: UUID = None, limit: int = Query(50, ge=1, le=50), offset: int = Query(0, ge=0)):
    filtered_subcategories = []
    if categoryId:
        for subcategory in subcategories:
            if subcategory.category_id == categoryId:
                filtered_subcategories.append(subcategory)

        if filtered_subcategories:
            return filtered_subcategories[offset:offset+limit]
        else:
            raise HTTPException(
                status_code=404, detail="Subcategories not found")
    return subcategories[offset:offset+limit]


@app.post("/v1/subcategories", response_model=SubCategory, status_code=201, tags=["subcategories"])
async def create_subcategory(new_subcategory: NewSubCategory):
    subcategory_id = (uuid.uuid4())
    subcategory = SubCategory(
        id=subcategory_id, name=new_subcategory.name, category_id=new_subcategory.category_id, image=new_subcategory.image)
    subcategories.append(subcategory)
    print(subcategory)
    with open('subcategories.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([subcategory_id, new_subcategory.category_id,
                        new_subcategory.name, new_subcategory.image])

    return subcategory


@app.get("/v1/subcategories/{subcategoryId}", status_code=200, response_model=SubCategory, tags=["subcategories"])
async def get_subcategory(subcategoryId: UUID):
    for subcategory in subcategories:
        if subcategory.id == subcategoryId:
            return subcategory
    raise HTTPException(status_code=404, detail="Subcategory not found")


@app.delete("/v1/subcategories/{subcategoryId}", status_code=204, tags=["subcategories"])
async def delete_subcategory(subcategoryId: UUID):
    for i, subcategory in enumerate(subcategories):
        if subcategory.id == subcategoryId:
            del subcategories[i]
            return
    raise HTTPException(status_code=404, detail="SubCategory not found")


@app.put("/v1/subcategories/{subcategoryId}", status_code=202, response_model=SubCategory, tags=["subcategories"])
async def update_subcategory(subcategoryId: UUID, updated_subcategory: SubCategory):
    for i, c in enumerate(subcategories):
        if c.id == subcategoryId:
            subcategories[i] = update_subcategory
            return update_subcategory
    raise HTTPException(status_code=404, detail="SubCategory not found")

# Products


@app.get("/v1/products", status_code=200, tags=["products"])
async def get_products(categoryId: UUID = None, subcategoryId: UUID = None, limit: int = Query(50, ge=1, le=50), offset: int = Query(0, ge=0)):
    if categoryId:
        filtered_products = [
            product for product in products if product.category_id == categoryId]
        if subcategoryId:
            filtered_products = [
                product for product in filtered_products if product.subcategory_id == subcategoryId]
    elif subcategoryId:
        filtered_products = [
            product for product in products if product.subcategory_id == subcategoryId]
    else:
        filtered_products = products

    total_products = len(filtered_products)
    if offset >= total_products:
        raise HTTPException(
            status_code=404, detail="Offset is greater than total products")
    if total_products == 0:
            raise HTTPException(
                status_code=404, detail="Products not found")
    return filtered_products[offset:offset+limit]


@app.post("/v1/products", response_model=Product, status_code=201, tags=["products"])
async def create_product(new_product: NewProduct):
    product_id = (uuid.uuid4())
    product = Product(id=product_id, name=new_product.name, description=new_product.description,
                      category_id=new_product.category_id, subcategory_id=new_product.subcategory_id, image=new_product.image)
    products.append(product)
    print(product)
    with open('products.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([product_id, new_product.name, new_product.description,
                        new_product.category_id, new_product.subcategory_id, new_product.image])

    return product


@app.get("/v1/products/{productId}", response_model=Product, tags=["products"])
async def get_product(productId: UUID):
    for product in products:
        if product.id == productId:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.put("/v1/products/{productId}", status_code=202, response_model=Product, tags=["products"])
async def update_product(productId: UUID, updated_product: Product):
    for i, p in enumerate(products):
        if p.id == productId:
            products[i] = update_product
            return update_product
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/v1/products/{productId}", status_code=204, tags=["products"])
async def delete_product(productId: UUID):
    for i, product in enumerate(products):
        if product.id == productId:
            del products[i]
            return
    raise HTTPException(status_code=404, detail="Product not found")