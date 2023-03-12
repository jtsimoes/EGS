import uvicorn
import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

app = FastAPI(openapi_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.exception_handler(404)
async def not_found_error(request: Request, exc: HTTPException):
    title = "404"
    return templates.TemplateResponse("404.html", {"request": request, "title": title}, status_code=404)

@app.exception_handler(502)
async def bad_gateway_error(request: Request, exc: HTTPException):
    title = "502"
    return templates.TemplateResponse("502.html", {"request": request, "title": title}, status_code=502)


@app.get("/")
async def index():
    ##### TODO: create index page design
    return {"message": "Welcome to main page!"}


@app.get("/items", response_class=HTMLResponse)
async def items(request: Request):

    # API call to get all items
    try:
        callAPI = requests.get("http://localhost:8000/products")    ##### TODO: Endpoint to get all items on stock database
        callAPI.close()
    except:
        raise HTTPException(status_code=504)

    # Check if API call was successful
    if not callAPI.ok:
        raise HTTPException(status_code=502)

    # Convert API response to JSON
    items = callAPI.json()

    title = "Lista"
    return templates.TemplateResponse("items.html", {"request": request, "title": title, "items": items})


@app.get("/items/{id}", response_class=HTMLResponse)
async def item(request: Request, id: str):
    if not "item found":    # check if item exists, if not return error
        raise HTTPException(status_code=404)

    details = {
        "id": id,
        "name": "Nome do item",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies ultricies, nunc nisl aliquam nunc, eget aliquam nisl nisl sit amet nisl. Nullam auctor, nisl eget ultricies ultricies, nunc nisl aliquam nunc, eget aliquam nisl nisl sit amet nisl. Nullam auctor, nisl eget ultricies ultricies, nunc nisl aliquam nunc, eget aliquam nisl nisl sit amet nisl.",
        "user": "Utilizador#1234",
        "category": "Carros",
        # float needed for correct formatting?? depends on the database
        "old_price": "{:.2f}".format(float(20)),
        # float needed for correct formatting?? depends on the database
        "price": "{:.2f}".format(float(10.3)),
        # float needed for correct formatting?? depends on the database
        "rating": float("{:.1f}".format(float(4.46))),
        "orders": 420,
        "reviews": 68,
        "image": "https://www.slntechnologies.com/wp-content/uploads/2017/08/ef3-placeholder-image.jpg",
        "quantity": 5,
        "availability": 2
    }
    details = json.dumps(details)

    details = json.loads(details)

    title = "Item"
    return templates.TemplateResponse("item.html", {"request": request, "title": title, "details": details})


@app.get("/messages", response_class=HTMLResponse)
async def messages(request: Request):
    messages = "TODO"

    title = "Mensagens"
    return templates.TemplateResponse("messages.html", {"request": request, "title": title, "messages": messages})


@app.get("/messages/{id}", response_class=HTMLResponse)
async def message(request: Request, id: str):
    message = "TODO"

    title = "NOME DO UTILIZADOR AQUI"
    return templates.TemplateResponse("message.html", {"request": request, "title": title, "message": message})


@app.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    title = "Checkout"
    return templates.TemplateResponse("checkout.html", {"request": request, "title": title})

if __name__ == "__main__":
    # TODO: using 'reload=True' for development environment only, remove for production
    uvicorn.run("main:app", host="127.0.0.1", port=80, reload=True)
