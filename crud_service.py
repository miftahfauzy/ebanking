from __future__ import absolute_import, print_function
import json
from decimal import Decimal
from datetime import datetime

from pony.converting import str2datetime
from pony.orm import *
from pony.orm.core import ObjectNotFound

from initdb_ebanking import *


# Customer Service
class CustomerService:
    @db_session
    def customer_list():
        arr_customer = []
        customers = Customer.select()

        for customer in customers:
            json_customer = {
                "customer_id": customer[0],
                "first_name": customer[1],
                "last_name": customer[2],
                "date_of_birth": customer[3],
                "email": customer[4],
                "insert_at": customer[5],
                "update_at": customer[6],
                "account_customer": customer[7],
                "bank_transaction": customer[8],
                "credit_card": customer[9],
                "load": customer[10],
                "address": customer[11],
            }
            arr_customer.append(json_customer)
        return arr_customer

    @db_session
    def get_customerbyid(cust_id):
        customer = Customer.get(customer_id=cust_id)
        if customer is None:
            result = {
                "status": 401,
                "message": "customer with id: " + str(cust_id) + " not found",
            }
            return result
        customer_dict = customer.to_dict()

        result = {
            "status": 200,
            "message": "customer found",
            # "customer": customer_dict
            "customer": {
                "customer_id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "date_of_birth": str(customer.date_of_birth),
                "email": customer.email,
                "account_customer": customer.account_customer,
                "bank_transaction": customer.bank_transaction,
                "credit_card": customer.credit_card,
                "loan": customer.loan,
                "address": customer.address,
                "insert_at": str(customer.insert_at),
                "update_at": str(customer.update_at),
            },
        }
        return result


# Address Service
class AddressService:
    @db_session
    def address_list():
        arr_address = []
        addresses = select(
            (
                a.address_id,
                a.street_address1,
                a.street_address2,
                a.city,
                a.zipcode,
                a.state,
                a.country,
                a.insert_at,
                a.update_at,
            )
            for a in Address
        )[:]

        for addr in addresses:
            json_address = {
                "address_id": addr[0],
                "street_address1": addr[1],
                "street_address2": addr[2],
                "city": addr[3],
                "zipcode": addr[4],
                "state": addr[5],
                "country": addr[6],
                "insert_at": str(addr[7]),
                "update_at": str(addr[8]),
            }
            arr_address.append(json_address)
        return arr_address

    @db_session
    def get_addressbyid(addr_id):
        address = Address.get(address_id=addr_id)
        if address is None:
            result = {
                "status": 404,
                "message": "Address with id: " + str(addr_id) + " not found",
            }
            return result
        address_dict = address.to_dict()
        result = {
            "status": 200,
            "message": "address found !",
            # "address": address_dict
            "address": {
                "address_id": address.address_id,
                "street_address1": address.street_address1,
                "street_address2": address.street_address2,
                "city": address.city,
                "zipcode": address.zipcode,
                "state": address.state,
                "country": address.country,
                "insert_at": str(address.insert_at),
                "update_at": str(address.update_at),
            },
        }

        return result

    @db_session
    def create_address(address_payload):
        address_parse = json.loads(json.dumps(address_payload))
        try:
            _address = Address(
                street_address1=address_parse["street_address1"],
                street_address2=address_parse["street_address2"],
                city=address_parse["city"],
                zipcode=address_parse["zipcode"],
                state=address_parse["state"],
                country=address_parse["country"],
                insert_at=datetime.now(),
            )
            commit()
            result = {
                "status": 201,
                "message": "address created !",
                # "address": _address.to_dict()
                # }
                "address": {
                    "address_id": _address.address_id,
                    "street_address1": _address.street_address1,
                    "street_address2": _address.street_address2,
                    "city": _address.city,
                    "zipcode": _address.zipcode,
                    "state": _address.state,
                    "country": _address.country,
                    "insert_at": str(_address.insert_at),
                    "update_at": str(_address.update_at),
                },
            }
            return result

        except KeyError as error:
            output = {
                "status": "Error : missing key/value of: " + str(error),
                "http status": 400,
                "address": address_parse,
            }
            return output

    @db_session
    def update_address(address_payload, address_id):
        address_parse = json.loads(json.dumps(address_payload))
        try:
            address = Address.get_for_update(address_id=address_id)
            address.street_address1 = address_parse["street_address1"]
            address.street_address2 = address_parse["street_address2"]
            address.city = address_parse["city"]
            address.zipcode = address_parse["zipcode"]
            address.state = address_parse["state"]
            address.country = address_parse["country"]
            address.update_at = datetime.now()
            commit()
            result = {
                "status": "Success",
                "message": "Success Update address",
                "address": {
                    "street_address1": address_parse["street_address1"],
                    "street_address2": address_parse["street_address2"],
                    "city": address_parse["city"],
                    "zzicode": address_parse["zipcode"],
                    "state": address_parse["state"],
                    "country": address_parse["country"],
                    "updated_at": str(datetime.now()),
                },
            }
            return result
        except ValueError:
            result = {
                "status": "Failed",
                "message": "Failed Update address",
                "address": {
                    "street_address1": address_parse["street_address1"],
                    "street_address2": address_parse["street_address2"],
                    "city": address_parse["city"],
                    "zzicode": address_parse["zipcode"],
                    "state": address_parse["state"],
                    "country": address_parse["country"],
                    "updated_at": str(datetime.now()),
                },
            }
            return result

    @db_session
    def delete_address(address_id):
        try:
            address_deleted = Address[address_id].delete()
        except ObjectNotFound:
            result = {
                "status": 404,
                "message": "Address with id: " + str(address_id) + " not found"
            }
            return result
        if address_deleted is None:
            result = {
                "status": 200,
                "message": "Address with id: " + str(address_id) + " Success Deleted"
            }
            return result


# if __name__ == "__main__":
    # print(CustomerService.customer_list())
    # print(CustomerService.get_customerbyid(1))
    # print(AddressService.get_addressbyid(1))
    # print(type(AddressService.get_addressbyid(1)))
    # print(CustomerService.address_list())
    print(AddressService.delete_address(1004))