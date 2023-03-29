# Stock API

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Test Data](#test_data)

## About <a name = "about"></a>

Stock API 
## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites


```
Python 3.7+
FastAPI
Uvicorn
SQLAlchemy
```

### Installing 


```
pip install -r requirements.txt
```

## Usage <a name = "usage"></a>
- Create the database
```
python3 database.py
```

- Run the server

```
uvicorn stockAPI:app --reload 
```

To change the port use --port
```
uvicorn stockAPI:app --reload --port 8080
```

To change the host use --host
```
uvicorn stpckAPI:app --reload --host 0.0.0.0
```

## Test Data <a name = "test_data"></a>

If you want to test with my data use the [Database Client](https://database-client.com/) visual studio extension and import the json files