import json
import asyncio
from json.decoder import JSONDecodeError
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from japronto import Application, RouteNotFoundException

from crud_service import *


class CustomerResource:
    def list_customer(request):
        customers = CustomerService.customer_list()
        return request.Response(json=customers)



