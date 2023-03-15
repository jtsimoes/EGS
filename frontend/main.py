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


@app.exception_handler(504)
async def gateway_timeout_error(request: Request, exc: HTTPException):
    title = "504"
    return templates.TemplateResponse("502.html", {"request": request, "title": title}, status_code=504)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # TODO: create index page design
    title = "Página inicial"
    return templates.TemplateResponse("index.html", {"request": request, "title": title})


@app.get("/items", response_class=HTMLResponse)
async def items(request: Request):

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

    items = [
        {"id": 1, "name": "Óculos de sol",              "user": "Sofia Oliveira",
            "image": "https://magento.opticalia.com/media/catalog/product/cache/e4be6767ec9b37c1ae8637aee2f57a6a/v/t/vts560910.png",     "price": "10",   "old_price": "15"},
        {"id": 2, "name": "Relógio de pulso",           "user": "Gabriel Santos",
            "image": "https://5.imimg.com/data5/KC/PC/MY-38629861/dummy-chronograph-watch-500x500.jpg",     "price": "1.4"},
        {"id": 3, "name": "Cadeira de escritório",      "user": "Marina Silva",
            "image": "https://1616346425.rsc.cdn77.org/temp/1615370739_6c9e04b9c72b4bcb5c03e722bff91b05.jpg",     "price": "2.99",    "old_price": "3.99"},
        {"id": 4, "name": "Smartphone",                 "user": "Lucas Costa",
            "image": "https://www.hisense.pt/wp-content/uploads/2019/06/H30-ICE-BLUE-1-2.png",     "price": "6.5"},
        {"id": 5, "name": "Calças de ganga",            "user": "Amanda Souza",
            "image": "https://traquinaskids.pt/42985-large_default/calca-ganga-indigo-tiffosi.jpg",     "price": "9.99"},
        {"id": 6, "name": "Caneca de café",             "user": "Pedro Alves",
            "image": "https://www.awnhillbrindes.com/shopeasy/produtos/resized/SP1052_420x560.png",     "price": "22"},
        {"id": 7, "name": "Mala de viagem",             "user": "Bianca Costa",
            "image": "https://img.joomcdn.net/57e3cb5b80a268ab3c8c28d13f7bcac81f21cc71_1024_1024.jpeg",     "price": "3.5"}
    ]

    title = "Lista"
    return templates.TemplateResponse("items.html", {"request": request, "title": title, "items": items})


@app.get("/items/{id}", response_class=HTMLResponse)
async def item(request: Request, id: str):
    if not "item found":    # check if item exists, if not return error
        raise HTTPException(status_code=404)

    details = {
        "id": id,
        "date": "2023-03-10 02:34:00",
        "name": "Nome do item",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies ultricies, nunc nisl aliquam nunc, eget aliquam nisl nisl sit amet nisl. Nullam auctor, nisl eget ultricies ultricies, nunc nisl aliquam nunc, eget aliquam nisl nisl sit amet nisl. Nullam auctor, nisl eget ultricies ultricies, nunc nisl aliquam nunc, eget aliquam nisl nisl sit amet nisl.",
        "user": "Nome do Utilizador",
        "category": "Carros",
        "old_price": "20",
        "price": "10.3",
        # float needed for correct formatting?? depends on the database
        # TODO: Move this to user profile
        "rating": float("{:.1f}".format(float(4.46))),
        "orders": 420,  # TODO: Move this to user profile
        "reviews": 68,  # TODO: Move this to user profile
        "image": "https://www.slntechnologies.com/wp-content/uploads/2017/08/ef3-placeholder-image.jpg",
        "quantity": 5,  # TODO: Remove this
        "location": "Aradas - Aveiro",
        "condition": "Usado",
        "availability": 1
    }
    details = json.dumps(details)

    details = json.loads(details)

    title = details["name"]
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


@app.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
    title = "Carinho"
    return templates.TemplateResponse("cart.html", {"request": request, "title": title})


@app.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    title = "Checkout"
    return templates.TemplateResponse("checkout.html", {"request": request, "title": title})

if __name__ == "__main__":
    # TODO: using 'reload=True' for development environment only, remove for production
    uvicorn.run("main:app", host="127.0.0.1", port=80, reload=True)
