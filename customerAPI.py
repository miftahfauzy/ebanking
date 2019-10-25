import json
import asyncio
from json.decoder import JSONDecodeError
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from japronto import Application, RouteNotFoundException

from crud_service import *


class CustomerResource:
    def list_customer(request):
        try:
            customers = CustomerService.customer_list()
            if len(customers) == 0:
                output = {
                    "status": 401, 
                    "message": "customer empty"
                    }
            else:
                output = {
                    "status": 200,
                    "message": "Success",
                    "customers": customers
                }
        except ValueError:
            output = {
                "status": 500,
                "message": "Server Error"
            }
        except TypeError as te:
            output = {
                "status": str(te),
                "http status": "Server Error",
                "customers": customers
            }
        return request.Response(code=output["status"], json=output)
    