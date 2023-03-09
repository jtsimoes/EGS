# Stock API

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

Stock API 
## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites


```
Python 3.7+
FastAPI
Uvicorn
```

### Installing


```
pip install -r requirements.txt
```


## Usage <a name = "usage"></a>

```
uvicorn stockAPI:app --reload 
```

To change the port use --port
```
uvicorn main:app --reload --port 8080
```

To change the host use --host
```
uvicorn main:app --reload --host 0.0.0.0
```
