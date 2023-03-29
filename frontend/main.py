import uvicorn
import json  # TODO: necessary?
import requests  # TODO: necessary?
from functools import lru_cache  # TODO: for cache
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
#import config  # TODO: for cache
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
    #return config.Settings()
    return None


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: Testing POST new user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # db_user = crud.get_user_by_email(db, email=user.email)
    # if db_user:
    # raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# TODO: Testing GET all users
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users


# TODO: Testing GET single user
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# TODO: Testing POST new item
@app.post("/items/new", response_model=schemas.Item)
def create_item_for_user(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


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
#async def index(request: Request, settings: config.Settings = Depends(get_settings)):
    # TODO: create index page design
    #test = settings.HELLO_WORLD
    #print("-------------->"+test)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
async def login():
    return RedirectResponse(url='//localhost:8000/authorize')

@app.get("/logout")
async def logout():
    return RedirectResponse(url='//localhost:8000/logout')


@app.get("/items", response_class=HTMLResponse)
async def items(request: Request, category: int = None, view: str = "grid", page: int = 0, limit: int = 9, sort: str = 'id', order: str = 'asc', db: Session = Depends(get_db)):
    
    items = crud.get_all_items(db, category, page, limit, sort, order)
    total = crud.count_items(db)


    # API call to get all items
    # try:
    # TODO: Endpoint to get all items on stock database
    #   callAPI = requests.get("http://localhost:8000/products")
    #   callAPI.close()
    # except:
    #   raise HTTPException(status_code=504)

    # Check if API call was successful
    # if not callAPI.ok:
    #   raise HTTPException(status_code=502)

    # Convert API response to JSON
    # items = callAPI.json()

    return templates.TemplateResponse("items.html", {"request": request, "items": items, "category": category, "view": view, "page": page, "limit": limit, "total": total})


@app.get("/items/{item_id}", response_class=HTMLResponse)
async def item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return templates.TemplateResponse("item.html", {"request": request, "item": item})


@app.get("/profiles", response_class=HTMLResponse)
async def profiles(request: Request):
    profiles = "TODO"

    return templates.TemplateResponse("404.html", {"request": request, "profiles": profiles})


@app.get("/profiles/{user_username}", response_class=HTMLResponse)
async def profile(request: Request, user_username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, user_username=user_username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


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

if __name__ == "__main__":
    # TODO: using 'reload=True' for development environment only, remove for production
    uvicorn.run("main:app", host="127.0.0.1", port=80, reload=True)
