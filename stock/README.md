# Stock API

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Test Data](#test_data)
- [Deployment](#deployment)

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
## Test Data <a name = "test_data"></a>

- Choose a SQL client tool in my case I use the [Database Client](https://database-client.com/) visual studio extension
- Connect to the remote database using the credentials listed in the [docker-compose](docker-compose.yml) file
  - To get the host, run the following command to see the container's IP
  ```docker inspect stockapi_db_1 | grep IPAddress ```
- Execute the SQL query presented in [data](data.sql) file


## Deployment <a name = "deployment"></a> 

```bash
#create the configmap for the stock database
kubectl create configmap mariadb-init-map -n egs-ressellr --from-file=./db/init.sql

# The rest of the deployment is done with the following commands

docker buildx build --platform linux/amd64 --network=host -t registry.deti:5000/egs-ressellr/stock:v3 -f Dockerfile.app .
docker push registry.deti:5000/egs-ressellr/stock:v3

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