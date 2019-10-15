import json
import asyncio
from json.decoder import JSONDecodeError
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound
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
                "customers": customers,
            }
        return request.Response(json=output)

    def get_customer(request):
        try:
            customer_id = int(request.match_dict["customer_id"])
            customers = CustomerService.get_customer(customer_id)
            output = {"status": "Success", "http status": 200, "customers": customers}
            return request.Response(json=output)
        except ValueError as ve:
            output = {
                "status": "Invalid parameter for /customer/{"
                + request.match_dict["customer_id"]
                + "}, customer ID -> '"
                + request.match_dict["customer_id"]
                + "' must integer type!",
                "http status": 500,
                "exception": str(ve),
            }
            return request.Response(code=500, json=output)
        except NoResultFound:
            output = {
                "status": "No record found! with customer ID: " + str(customer_id),
                "http status": 404,
                "customers": {},
            }
            return request.Response(code=404, json=output)
        except RouteNotFoundException as noRoute:
            output = {
                "status": "Invalid parameter for /customer/{"
                + request.match_dict["customer_id"]
                + "}, customer ID -> '"
                + request.match_dict["customer_id"]
                + "' must integer type!",
                "http status": 404,
                "exception": str(noRoute),
            }
            return request.Response(code=500, json=output)

    def create_customer(request):
        try:
            vcustomer = request.json
        except JSONDecodeError as jsonerror:
            output = {
                "status": "Error: 400 Bad Request",
                "description": "Empty/incomplete on request body, A valid JSON document is required!",
                "http status": 400,
            }
            return request.Response(code=400, json=output)

        except ValueError as ve:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(ve),
                "http status": 400,
            }
            return request.Response(code=400, json=output)

        customer = {}
        output = {}
        try:
            customer = customerService.create(vcustomer)
            return request.Response(code=201, json=customer)
        except KeyError as error:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(error),
                "http status": 400,
                "customer": customer,
            }
            return request.Response(code=400, json=output)

    def update_customer(request):
        try:
            vcustomer = request.json
        except JSONDecodeError as jsonerror:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(jsonerror) + " on JSON request body !",
                "http status": 400,
            }
            return request.Response(code=400, json=output)
        try:
            customer_id = int(request.match_dict["customer_id"])
        except ValueError as ve:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(ve),
                "http status": 400,
            }
            return request.Response(code=400, json=output)

        customer = {}
        output = {}

        try:
            updated_customer = CustomerService.update_customer(vcustomer, customer_id)
            output = {
                "status": "Success Updated",
                "http status": 200,
                "customer": updated_customer,
            }
            return request.Response(code=200, json=output)
        except KeyError as error:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(error),
                "http status": 400,
                "customer": customer,
            }
            return request.Response(code=400, json=output)

    def delete_customer(request):
        # if request.match_dict['customer_id']:

        try:
            print("query reques : " + str(request.match_dict))
        except KeyError as error:
            output = {
                "status": "Error: 400 Bad Request",
                "description": "Request param on /customer/delete/{"
                + str(error)
                + "} was no provided",
                "http status": 400,
            }
            return request.Response(code=400, json=output)

        try:
            _customer_id = int(request.match_dict["customer_id"])
        except ValueError as ve:
            output = {
                "status": "Error: 400 Bad Request",
                "description": "Request param /customer/delete/{customer_id} must integer type!, but you input: "
                + str(request.match_dict),
                "http status": 400,
            }
            return request.Response(code=400, json=output)
        try:
            result = CustomerService.delete_customer(_customer_id)
            return request.Response(code=200, json=result)
        except ValueError as ve:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(ve),
                "http status": 400,
            }
            return request.Response(code=400, json=output)
        except RouteNotFoundException as noRoute:
            output = {
                "status": "Invalid parameter for /customer/delete/ "
                + request.match_dict["customer_id"],
                "http status": 404,
                "exception": str(noRoute),
            }
            return request.Response(code=404, json=output)
        except Exception as ex:
            raise customerError()
