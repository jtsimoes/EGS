# Stock API

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Deployment](#deployment)
- [Documentation](#documentation)

## About <a name = "about"></a>

The Stock API is a powerful tool that enables seamless management of products, categories, and subcategories within a stock or inventory system. Designed to simplify and streamline stock management processes, this API provides a set of features for organizing and tracking products across various categories and subcategories.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites


```
Python 3.7+
FastAPI
Uvicorn
SQLAlchemy
PyMySQL
MariaDB
Docker
Docker Compose
```

### Installing 


```
sudo docker-compose build
```

## Usage <a name = "usage"></a>
```
sudo docker-compose up
```


## Deployment <a name = "deployment"></a> 

This instruction is to use in a private server so you probably don't have access to that, change the commands to your requisits.

```bash
#create the configmap for the stock database
kubectl create configmap mariadb-init-map -n egs-ressellr --from-file=./db/init.sql

# The rest of the deployment is done with the following commands

docker buildx build --platform linux/amd64 --network=host -t registry.deti:5000/egs-ressellr/stock:v3.1 -f Dockerfile.app .
docker push registry.deti:5000/egs-ressellr/stock:v3.1

kubectl apply -f db-deployment.yaml
kubectl apply -f app-deployment.yaml

#Delete deployment
kubectl delete -f db-deployment.yaml
kubectl delete -f app-deployment.yaml

# Get all the pods in the namespace
kubectl get pods -n egs-ressellr

# Get all the services in the namespace
kubectl get services -n egs-ressellr

```

## Documentation <a name = "documentation"></a>
<a href="https://app.swaggerhub.com/apis-docs/Resellr/StockAPI/1.0.0"> SwaggerHub</a>