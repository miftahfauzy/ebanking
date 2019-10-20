import json
import asyncio
from json.decoder import JSONDecodeError
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from japronto import Application, RouteNotFoundException

from crud_service import *


class AddressResource:
    def list_address(request):
        addresses = AddressService.address_list()
        if len(addresses) == 0:
            result = {"status": 401, "message": "address empty"}
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
                "exception: ": str(ve),
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

        addressbyid = AddressService.get_addressbyid(id)
        if addressbyid["status"] == 404:
            result = {"status": 404, "message": "address not found!"}
            return request.Response(code=404, json=result)

        return request.Response(code=200, json=addressbyid)

    def address_create(request):
        try:
            address_json = request.json
        except JSONDecodeError:
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
        address = {}
        output = {}
        try:
            address = AddressService.create_address(address_json)
            return request.Response(code=201, json=address)
        except KeyError as error:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(error),
                "http status": 400,
                "address": address,
            }
            return request.Response(code=400, json=output)

    def address_update(request):
        try:
            address_json = request.json
        except JSONDecodeError:
            output = {
                "status": "Error: 400 Bad Request",
                "description": "Empty/incomplete on request body, A valid JSON document is required!",
                "http status": 400,
            }
            return request.Response(code=400, json=output)
        try:
            address_id = int(request.match_dict["address_id"])
        except ValueError as ve:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(ve),
                "http status": 400,
            }
            return request.Response(code=400, json=output)

        arr_address = {}
        output = {}

        try:
            updated_address = AddressService.update_address(address_json, address_id)
            output = {
                "status": "Success Updated",
                "http status": 200,
                "address": updated_address,
            }
            return request.Response(code=200, json=output)
        except KeyError as error:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(error),
                "http status": 400,
                "address": address_json,
            }
            return request.Response(code=400, json=output)


    def address_delete(request):
        try:
            address_json = request.json
        except JSONDecodeError:
            output = {
                "status": "Error: 400 Bad Request",
                "description": "Empty/incomplete on request body, A valid JSON document is required!",
                "http status": 400,
            }
            return request.Response(code=400, json=output)
        try:
            address_id = int(request.match_dict["address_id"])
        except ValueError as ve:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(ve),
                "http status": 400,
            }
            return request.Response(code=400, json=output)

        arr_address = {}
        output = {}

        try:
            updated_address = AddressService.delete_address(address_json, address_id)
            output = {
                "status": "Success Deleted",
                "http status": 200,
                "address": updated_address,
            }
            return request.Response(code=200, json=output)
        except KeyError as error:
            output = {
                "status": "Error: 400 Bad Request",
                "description": str(error),
                "http status": 400,
                "address": address_json,
            }
            return request.Response(code=400, json=output)
