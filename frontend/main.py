import uvicorn
import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

app = FastAPI(title="Resellr", description="Buy & Sell", version="1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


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
    # TODO: create index page design
    title = "Página inicial"
    return templates.TemplateResponse("index.html", {"request": request, "title": title})
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/logout")
async def logout():
    return RedirectResponse(url='//localhost:5000/authorize')

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
        {"id": 1, "name": "Óculos de sol",              "user": "Sofia Oliveira",   "location": "Aradas (Aveiro)",      "date": "2023-03-16 19:37:00",
            "image": "https://magento.opticalia.com/media/catalog/product/cache/e4be6767ec9b37c1ae8637aee2f57a6a/v/t/vts560910.png",     "price": "10",   "old_price": "15",  "availability": 1},
        {"id": 2, "name": "Relógio de pulso",           "user": "Gabriel Santos",   "location": "Mafra (Lisboa)",       "date": "2023-02-10 12:34:00",
            "image": "https://5.imimg.com/data5/KC/PC/MY-38629861/dummy-chronograph-watch-500x500.jpg",     "price": "1.4",  "availability": 1},
        {"id": 3, "name": "Cadeira de escritório",      "user": "Marina Silva",     "location": "Lisboa (Lisboa)",      "date": "2022-03-10 12:34:00",
            "image": "https://1616346425.rsc.cdn77.org/temp/1615370739_6c9e04b9c72b4bcb5c03e722bff91b05.jpg",     "price": "2.99",    "old_price": "3.99",  "availability": 1},
        {"id": 4, "name": "Smartphone",                 "user": "Lucas Costa",      "location": "Gouveia (Guarda)",     "date": "2023-03-01 12:34:00",
            "image": "https://www.hisense.pt/wp-content/uploads/2019/06/H30-ICE-BLUE-1-2.png",     "price": "6.5",  "availability": 1},
        {"id": 5, "name": "Calças de ganga",            "user": "Amanda Souza",     "location": "Tomar (Santarém)",     "date": "2020-03-10 12:34:00",
            "image": "https://traquinaskids.pt/42985-large_default/calca-ganga-indigo-tiffosi.jpg",     "price": "9.99",  "availability": 1},
        {"id": 6, "name": "Caneca de café",             "user": "Pedro Alves",      "location": "Estarreja (Aveiro)",   "date": "2023-03-15 21:34:00",
            "image": "https://www.awnhillbrindes.com/shopeasy/produtos/resized/SP1052_420x560.png",     "price": "22",  "availability": 1},
        {"id": 7, "name": "Mala de viagem",             "user": "Bianca Costa",     "location": "Gaia (Porto)",         "date": "2023-03-10 12:34:00",
            "image": "https://img.joomcdn.net/57e3cb5b80a268ab3c8c28d13f7bcac81f21cc71_1024_1024.jpeg",     "price": "3.5",  "availability": 0}
    ]

    return templates.TemplateResponse("items.html", {"request": request, "items": items})


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
        "phone": 123456789,  # TODO: Move this to user profile
        "registration": "2022-01-10 02:34:00",  # TODO: Move this to user profile
        "image": "https://www.slntechnologies.com/wp-content/uploads/2017/08/ef3-placeholder-image.jpg",
        "quantity": 5,  # TODO: Remove this
        "location": "Aradas (Aveiro)",
        "condition": "Usado",
        "availability": 1
    }
    details = json.dumps(details)

    details = json.loads(details)

    return templates.TemplateResponse("item.html", {"request": request, "details": details})


@app.get("/profiles", response_class=HTMLResponse)
async def profiles(request: Request):
    profiles = "TODO"

    return templates.TemplateResponse("404.html", {"request": request, "profiles": profiles})


@app.get("/profiles/{id}", response_class=HTMLResponse)
async def profile(request: Request, id: str):
    profile = {
        "id": id,
        "name": "Nome do Utilizador",
        "email": "utilizador@user.pt",
        "rating": float("{:.1f}".format(float(4.46))),
        "amount_sales": 420,
        "amount_purchases": 333,
        "reviews": 68,
        "phone": 123456789,
        "registration": "2022-01-10 02:34:00",
        "location": "Aradas (Aveiro)",
        "avatar": "https://www.w3schools.com/howto/img_avatar.png"
    }

    items = [
        {"id": 1, "name": "Óculos de sol",              "user": profile["id"],   "location": "Lisboa (Lisboa)",      "date": "2023-03-16 19:37:00",
            "image": "https://magento.opticalia.com/media/catalog/product/cache/e4be6767ec9b37c1ae8637aee2f57a6a/v/t/vts560910.png",     "price": "10",   "old_price": "15",  "availability": 1},
        {"id": 2, "name": "Relógio de pulso",           "user": profile["id"],   "location": "Mafra (Lisboa)",       "date": "2023-02-10 12:34:00",
            "image": "https://5.imimg.com/data5/KC/PC/MY-38629861/dummy-chronograph-watch-500x500.jpg",     "price": "1.4",  "availability": 0},
        {"id": 3, "name": "Cadeira de escritório",      "user": profile["id"],     "location": "Lisboa (Lisboa)",      "date": "2022-03-10 12:34:00",
            "image": "https://1616346425.rsc.cdn77.org/temp/1615370739_6c9e04b9c72b4bcb5c03e722bff91b05.jpg",     "price": "2.99",    "old_price": "3.99",  "availability": 1},
        {"id": 4, "name": "Smartphone",                 "user": profile["id"],      "location": "Oeiras (Lisboa)",     "date": "2023-03-01 12:34:00",
            "image": "https://www.hisense.pt/wp-content/uploads/2019/06/H30-ICE-BLUE-1-2.png",     "price": "6.5",  "availability": 1}
    ]

    return templates.TemplateResponse("profile.html", {"request": request, "profile": profile, "items": items})


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
