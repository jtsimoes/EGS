from typing import Union
from http.client import HTTPException
import json
import uuid
from fastapi import FastAPI, Query, Header
from uuid import UUID
from pydantic import BaseModel, Field

app = FastAPI(title="Payment API", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Server is UP"}

@app.get("/checkout/orders/{id}")
async def getOrder():
    return """[
        {
  "id": "5O190127TN364715T",
  "status": "APPROVED",
  "intent": "CAPTURE",
  "payment_source": {
    "paypal": {
      "name": {
        "given_name": "John",
        "surname": "Doe"
      },
      "email_address": "customer@example.com",
      "account_id": "QYR5Z8XDVJNXQ"
    }
  },
  "purchase_units": [
    {
      "reference_id": "d9f80740-38f0-11e8-b467-0ed5f89f718b",
      "amount": {
        "currency_code": "USD",
        "value": "100.00"
      }
    }
  ],
  "payer": {
    "name": {
      "given_name": "John",
      "surname": "Doe"
    },
    "email_address": "customer@example.com",
    "payer_id": "QYR5Z8XDVJNXQ"
  },
  "create_time": "2018-04-01T21:18:49Z",
  "links": [
    {
      "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
      "rel": "self",
      "method": "GET"
    },
    {
      "href": "https://www.paypal.com/checkoutnow?token=5O190127TN364715T",
      "rel": "approve",
      "method": "GET"
    },
    {
      "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
      "rel": "update",
      "method": "PATCH"
    },
    {
      "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T/capture",
      "rel": "capture",
      "method": "POST"
    }
  ]
}
]"""

@app.post("/checkout/orders")
async def createOrder():
    return """[
  "id": "5O190127TN364715T",
  "status": "PAYER_ACTION_REQUIRED",
  "payment_source": {
    "paypal": {}
  },
  "links": [
    {
      "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
      "rel": "self",
      "method": "GET"
    },
    {
      "href": "https://www.paypal.com/checkoutnow?token=5O190127TN364715T",
      "rel": "payer-action",
      "method": "GET"
    }
  ]
}]"""

@app.get("/payments/authorizations/{authorization_id}")
async def getPayment():
    return """[{
  "id": "0VF52814937998046",
  "status": "CREATED",
  "amount": {
    "value": "10.99",
    "currency_code": "USD"
  },
  "invoice_id": "INVOICE-123",
  "seller_protection": {
    "status": "ELIGIBLE",
    "dispute_categories": [
      "ITEM_NOT_RECEIVED",
      "UNAUTHORIZED_TRANSACTION"
    ]
  },
  "expiration_time": "2017-10-10T23:23:45Z",
  "create_time": "2017-09-11T23:23:45Z",
  "update_time": "2017-09-11T23:23:45Z",
  "links": [
    {
      "rel": "self",
      "method": "GET",
      "href": "https://api-m.paypal.com/v2/payments/authorizations/0VF52814937998046"
    },
    {
      "rel": "capture",
      "method": "POST",
      "href": "https://api-m.paypal.com/v2/payments/authorizations/0VF52814937998046/capture"
    },
    {
      "rel": "void",
      "method": "POST",
      "href": "https://api-m.paypal.com/v2/payments/authorizations/0VF52814937998046/void"
    },
    {
      "rel": "reauthorize",
      "method": "POST",
      "href": "https://api-m.paypal.com/v2/payments/authorizations/0VF52814937998046/reauthorize"
    }
  ]
}]"""

@app.post("/payments/authorizations/{authorization_id}/capture")
async def createPayment():
    return """[{
  "id": "2GG279541U471931P",
  "status": "COMPLETED",
  "links": [
    {
      "rel": "self",
      "method": "GET",
      "href": "https://api-m.paypal.com/v2/payments/captures/2GG279541U471931P"
    },
    {
      "rel": "refund",
      "method": "POST",
      "href": "https://api-m.paypal.com/v2/payments/captures/2GG279541U471931P/refund"
    },
    {
      "rel": "up",
      "method": "GET",
      "href": "https://api-m.paypal.com/v2/payments/authorizations/0VF52814937998046"
    }
  ]
}]"""
