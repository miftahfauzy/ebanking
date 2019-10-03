import json
import asyncio
from json.decoder import JSONDecodeError
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from japronto import Application, RouteNotFoundException

from customerSVC import *


class CustomerResource:
    def list_customer(request):
        customers = CustomerService.customer_list()
        return request.Response(json=customers)

    def list_address(request):
        addresses = CustomerService.address_list()
        if len(addresses) == 0:
            result = {
                "status": 401,
                "message": "address empty"
            }
            return request.Response(code=401, json=result)
        return request.Response(code=200, json=addresses)

    def getaddressbyid(request):
        try:
            id = int(request.match_dict["address_id"])
        except ValueError as ve:
            output = {
                "status": "Invalid parameter for address/{"
                + request.match_dict["address_id"]
                + "}, Address ID -> '"
                + request.match_dict["address_id"]
                + "' must integer type!",
                "http status: ": 500,
                "exception: ": str(ve)
            }
            return request.Response(code=500, json=output)
        except RouteNotFoundException as noRoute:
            output = {
                "status": "Invalid parameter for /address/{"
                + request.match_dict["address_id"]
                + "}, Product ID -> '"
                + request.match_dict["address_id"]
                + "' must integer type!",
                "http status": 404,
                "exception": str(noRoute),
            }
            return request.Response(code=500, json=output)

        addressbyid = CustomerService.get_addressbyid(id)
        if len(addressbyid) == 0:
            result = {
                "status": 401,
                "message": "address not found!"
            }
            return request.Response(code=401, json=result)
            pass
        return request.Response(code=200, json=addressbyid)

