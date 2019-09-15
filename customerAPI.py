import json
import asyncio
from json.decoder import JSONDecodeError
from marshmallow import ValidationError
from japronto import Application, RouteNotFoundException

from crud_service import *


class CustomerError(Exception):
    def __init__(self):
        self.msg = str(Exception)


class CustomerResource:
    def customer_not_found(request, exception):
        output = {
            "status": 404,
            "http status": "Request Not Found",
            "description": "request query : " + str(request.route),
        }
        return request.Response(code=404, json=output)

    def unhandled(request):
        1 / 0

    def list_customer(request):
        try:
            customers = CustomerService.customer_list()
            if len(customers) != 0:
                output = {"status": "Success", "http status": 200, "customers": customers}
            else:
                output = {
                    "status": "No record found!",
                    "http status": 401,
                    "exception": 401,
                    "customers": customers
                }
        except CustomerError as ex:
            output = {
                "status": str(ex),
                "http status": "Server Error",
                "exception": 501,
                "products": customers,
            }
        return request.Response(json=output)

