# Deployment

APIs put in docker containers

Run the following commands from the /EGS/ folder to see the APIs running

## Authentication

**build** -> docker build -t auth:1.0 -f deploy\Dockerfile.auth .\authentication
**run** -> docker run --rm -p 5000:5000 auth:1.0

## Frontend

**build** -> docker build -t frontend:1.0 -f deploy\Dockerfile.frontend .\frontend
**run** -> docker run --rm -p 80:80 frontend:1.0

## Messages

**build** -> docker build -t messages:1.0 -f deploy\Dockerfile.messages .\messages
**run** -> docker run --rm -p 3000:3000 messages:1.0

## Payment

**build** -> docker build -t payment:1.0 -f deploy\Dockerfile.payment .\payment
**run** -> docker run --rm -p 4000:4000 payment:1.0

## Stock

**build** -> docker build -t stock:1.0 -f deploy\Dockerfile.stock .\stock
**run** -> docker run --rm -p 8080:8080 stock:1.0
