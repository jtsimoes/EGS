FROM python:3.9-slim-buster

WORKDIR /stock

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/. .

EXPOSE 8000

CMD ["uvicorn", "stockAPI:app", "--host", "0.0.0.0", "--port", "8000"] 

