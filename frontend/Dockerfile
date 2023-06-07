FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /frontend

COPY ./app/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 80

#CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# build -> docker build -t frontend:1.0 -f deploy\Dockerfile.frontend .\frontend
# run -> docker run --rm -p 80:80 frontend:1.0