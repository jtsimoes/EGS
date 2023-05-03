import uvicorn
import json  # TODO: necessary?
import requests  # TODO: necessary?
from functools import lru_cache  # TODO: for cache
from typing import List
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
# import config  # TODO: for cache
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resellr", description="Buy & Sell", version="1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@lru_cache()
def get_settings():
    # return config.Settings()
    return None


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_all_categories():
    try:
        # TODO: Endpoint to get all categories
        response = requests.get("http://localhost:8000/v1/categories")
        response.close()
    except:
        raise HTTPException(status_code=504)

    # Check if API call was successful
    if not response.ok:
        raise HTTPException(status_code=502)

    # Convert API response to JSON
    categories = response.json()

    return categories


def get_category(category_id: int):
    try:
        # TODO: Endpoint to get one subcategory
        response = requests.get(
            "http://localhost:8000/v1/subcategories/" + str(category_id))
        response.close()
    except:
        raise HTTPException(status_code=504)

    # Check if API call was successful

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Category not found")

    if not response.ok:
        raise HTTPException(status_code=502)

    # Convert API response to JSON
    category = response.json()

    return category


# TODO: Testing POST new user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # db_user = crud.get_user_by_email(db, email=user.email)
    # if db_user:
    # raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# TODO: Testing GET all users
@app.get("/users/", response_model=List[schemas.User])
def read_users(page: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db, page, limit)
    return users


# TODO: Testing GET single user
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.exception_handler(404)
async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)


@app.exception_handler(502)
async def bad_gateway_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("502.html", {"request": request}, status_code=502)


@app.exception_handler(504)
async def gateway_timeout_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("502.html", {"request": request}, status_code=504)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # async def index(request: Request, settings: config.Settings = Depends(get_settings)):
    # test = settings.HELLO_WORLD
    # print("-------------->"+test)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", summary="LOOOOL", responses={
    403: {"description": "Not enough privileges"},
    404: {"description": "Item not found"},
    200: {
        "description": "Item requested by ID",
        "content": {
            "application/json": {
                "example": {
                    "id": "bar",
                    "value": "The bar tenders"
                },
                "schema": {
                    "$ref": "#/components/schemas/Item"
                }
            },
            "text/plain": {
                "schema": {
                    "type": "string",
                    "example": 'whoa!'
                }
            },
            "image/png": {}
        }
    },
    422: {
        "description": "Validation Error (default behavior)",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/HTTPValidationError"
                }
            }
        }
    }
})
async def login():
    return RedirectResponse(url="//localhost:8000/authorize")


@app.get("/logout")
async def logout():
    return RedirectResponse(url="//localhost:8000/logout")


@app.post("/items")
async def new_item(title: str = Form(...), description: str = Form(...), price: str = Form(...), image: str = Form("/static/images/misc/item.jpg"),
                   location: str = Form(...), condition: str = Form(...), category_id: str = Form(...), db: Session = Depends(get_db)):
    try:
        item = schemas.ItemCreate(title=title, description=description, price=price, image=image, location=location, condition=condition,
                                  owner_id=3,               # TODO: Obtain owner/user ID from login session
                                  category_id=category_id,  # TODO: Obtain category ID from categories API
                                  product_id=99999999999)   # TODO: Obtain product ID from products API

        new_item = crud.create_item(db=db, item=item)
    except:
        raise HTTPException(status_code=502, detail="Item not created")

    return RedirectResponse(url="/items/" + str(new_item.id), status_code=303)


@app.get("/items", response_class=HTMLResponse)
async def items(request: Request, category: int = None, view: str = "grid", page: int = 0, limit: int = 9, sort: str = 'id', order: str = 'asc', db: Session = Depends(get_db)):

    items = crud.get_all_items(db, category, page, limit, sort, order)
    total = crud.count_items(db)

    categories = get_all_categories()

    if category is not None:
        category = get_category(category)

    return templates.TemplateResponse("items.html", {"request": request, "items": items, "category": category, "view": view, "page": page, "limit": limit, "total": total, "categories": categories})


@app.get("/items/{item_id}", response_class=HTMLResponse)
async def item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return templates.TemplateResponse("item.html", {"request": request, "item": item})


@app.post("/items/delete/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    if not crud.delete_item(db, item_id):
        raise HTTPException(status_code=502, detail="Item not deleted")

    return RedirectResponse(url="/profiles", status_code=303)


@app.get("/profiles")
async def profiles():
    # TODO: Instead of showing all users, this endpoint will redirect to the profile of the logged in user
    # user = current_user.username
    user = "Username"

    return RedirectResponse(url="/profiles/"+user)


@app.get("/profiles/{user_username}", response_class=HTMLResponse)
async def profile(request: Request, user_username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, user_username=user_username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    categories = get_all_categories()

    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "categories": categories})


@app.get("/messages", response_class=HTMLResponse)
async def messages(request: Request):
    messages = "TODO"

    return templates.TemplateResponse("messages.html", {"request": request, "messages": messages})


@app.get("/messages/{id}", response_class=HTMLResponse)
async def message(request: Request, id: str):
    message = "TODO"

    return templates.TemplateResponse("message.html", {"request": request, "message": message})


@app.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


@app.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    return templates.TemplateResponse("checkout.html", {"request": request})


@app.get("/payment/{cart_json}")
async def payment(cart_json: str):

    cart_json = cart_json.replace("product_id", "id").replace(
        "product_price", "price").replace("product_name", "name")
    cart_json = json.loads(cart_json)

    try:
        # TODO: Endpoint to send to paypal
        # payload = dict(key1='value1', key2='value2')
        response = requests.post(
            "http://localhost:4000/create-order", data=cart_json)

        response.close()
    except:
        raise HTTPException(status_code=504)

    # Check if API call was successful
    if not response.ok:
        raise HTTPException(status_code=502)

    return "SUCCESS!"
