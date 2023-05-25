FROM python:alpine3.17

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade -r requirements.txt

COPY ./ .

EXPOSE 7000

CMD [ "python", "googleAuth.py"]
