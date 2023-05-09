from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from sqlalchemy.exc import IntegrityError
import models, schemas
import logging
import pymysql

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

models.Base.metadata.create_all(bind=engine)



app = FastAPI(title="Inventory API", version="1.0.0")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.get("/")
async def root():
    return {"message": "Server is UP"}


# Categories


@app.get("/v1/categories", response_model=List[schemas.Category], status_code=200, tags=["categories"])
async def get_categories(limit: int = Query(50, ge=1, le=50), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    categories = db.query(models.Category)
    total_categories = categories.count()
    if offset >= total_categories:
        raise HTTPException(status_code=404, detail="Offset is greater than total categories")    
    return categories.offset(offset).limit(limit).all()


@app.post("/v1/categories", response_model=schemas.Category, status_code=201, tags=["categories"])
async def create_category(new_category: schemas.NewCategory, db: Session = Depends(get_db)):
    category = models.Category(name=new_category.name, image=new_category.image)
    db.add(category)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Category with this name already exists")
    db.refresh(category)
    return category


@app.get("/v1/categories/{category_id}", response_model=schemas.Category, status_code=200, tags=["categories"])
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    print(category)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.delete("/v1/categories/{category_id}", status_code=204, tags=["categories"])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()


@app.put("/v1/categories/{category_id}", status_code=202, response_model=schemas.Category, tags=["categories"])
async def update_category(category_id: int, updated_category: schemas.NewCategory, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        category.id = category_id
        category.name = updated_category.name
        category.image = updated_category.image
        db.commit()
        return category
    raise HTTPException(status_code=404, detail="Category not found")


# Subcategories

@app.get("/v1/subcategories", status_code=200, tags=["subcategories"])
async def get_subcategories(category_id: int = None, limit: int = Query(50, ge=1, le=50),offset: int = Query(0, ge=0),db: Session = Depends(get_db)):
    filtered_subcategories = []
    if category_id:
        filtered_subcategories = db.query(models.SubCategory).filter(models.SubCategory.category_id == category_id).offset(offset).limit(limit).all()
        if not filtered_subcategories:
            raise HTTPException(status_code=404, detail="Subcategories not found")
    else:
        filtered_subcategories = db.query(models.SubCategory).offset(offset).limit(limit).all()

    return filtered_subcategories


@app.post("/v1/subcategories", response_model=schemas.SubCategory, status_code=201, tags=["subcategories"])
async def create_subcategory(new_subcategory: schemas.NewSubCategory, db: Session = Depends(get_db)):
    subcategory = models.SubCategory(
         name=new_subcategory.name, category_id=new_subcategory.category_id, image=new_subcategory.image)
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory) 
    return subcategory


@app.get("/v1/subcategories/{subcategoryId}", status_code=200, response_model=schemas.SubCategory, tags=["subcategories"])
async def get_subcategory(subcategoryId: int, db: Session = Depends(get_db)):
    subcategory = db.query(models.SubCategory).filter(models.SubCategory.id == subcategoryId).first()
    if subcategory:
        return subcategory
    raise HTTPException(status_code=404, detail="Subcategory not found")


@app.delete("/v1/subcategories/{subcategoryId}", status_code=204, tags=["subcategories"])
async def delete_subcategory(subcategoryId: int, db: Session = Depends(get_db)):
    subcategory = db.query(models.SubCategory).filter(models.SubCategory.id == subcategoryId).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    db.delete(subcategory)
    db.commit()



@app.put("/v1/subcategories/{subcategoryId}", status_code=202, response_model=schemas.SubCategory, tags=["subcategories"])
async def update_subcategory(subcategoryId: int, updated_subcategory: schemas.NewSubCategory, db: Session = Depends(get_db)):
    subcategory = db.query(models.SubCategory).filter(models.SubCategory.id == subcategoryId).first()
    if subcategory:
        subcategory.id = subcategoryId
        subcategory.name = updated_subcategory.name
        subcategory.category_id = updated_subcategory.category_id
        subcategory.image = updated_subcategory.image
        db.commit()
        return subcategory
    raise HTTPException(status_code=404, detail="SubCategory not found")

# Products

@app.get("/v1/products", status_code=200, tags=["products"])
async def get_products(categoryId: int = None, subcategoryId: int = None, limit: int = Query(50, ge=1, le=50), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    if categoryId and not subcategoryId:
        products_query = products_query = db.query(models.Product).filter(models.Product.category_id == categoryId)

    if subcategoryId and not categoryId:
        products_query = products_query = db.query(models.Product).filter(models.Product.subcategory_id == subcategoryId)

    if subcategoryId and categoryId:
        products_query = products_query = db.query(models.Product).filter(models.Product.subcategory_id == subcategoryId).filter(models.Product.category_id == categoryId)
    
    if not subcategoryId and not categoryId:
        products_query = db.query(models.Product)


    products = products_query.offset(offset).limit(limit).all()

    if not products:
        raise HTTPException(status_code=404, detail="Products not found")

    return products


@app.post("/v1/products", response_model=schemas.Product, status_code=201, tags=["products"])
async def create_product(new_product: schemas.NewProduct, db: Session = Depends(get_db)):
    product = models.Product(name=new_product.name, description=new_product.description,
                      category_id=new_product.category_id, subcategory_id=new_product.subcategory_id, image=new_product.image)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get("/v1/products/{productId}", response_model=schemas.Product, tags=["products"])
async def get_product(productId: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == productId).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/v1/products/{productId}", status_code=202, response_model=schemas.Product, tags=["products"])
async def update_product(productId: int, updated_product: schemas.NewProduct, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == productId).first()
    if product:
        product = updated_product
        db.commit()
        return updated_product
    raise HTTPException(status_code=404, detail="Product not found")
  
    


@app.delete("/v1/products/{productId}", status_code=204, tags=["products"])
async def delete_product(productId: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == productId).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()