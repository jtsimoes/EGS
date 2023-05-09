FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /stock

COPY ./app/requirements.txt requirements.txt

RUN pip3 install --upgrade -r requirements.txt

COPY ./app .

CMD [ "uvicorn", "stockAPI:app", "--reload", "--port", "6000", "--host", "0.0.0.0"]

# build -> docker build -t stock:1.0 -f deploy\Dockerfile.stock .\stock
# run -> docker run --rm -p 8080:8080 stock:1.0