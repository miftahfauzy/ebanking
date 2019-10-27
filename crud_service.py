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
        customers = select(
            (
                c.customer_id,
                c.first_name,
                c.last_name,
                c.date_of_birth,
                c.email,
                c.insert_at,
                c.update_at,
                c.account_customer,
                c.bank_transaction,
                c.credit_card,
                c.loan,
                c.address
            )
            for c in Customer
        )[:]

        for customer in customers:
            json_customer = {
                "customer_id": customer[0],
                "first_name": customer[1],
                "last_name": customer[2],
                "date_of_birth": str(customer[3]),
                "email": customer[4],
                "insert_at": str(customer[5]),
                "update_at": str(customer[6]),
                "account_customer": customer[7],
                "bank_transaction": customer[8],
                "credit_card": customer[9],
                "loan": customer[10],
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

    @db_session
    def create_customer(customer_payload):
        customer_parse = json.loads(json.dumps(customer_payload))
        try:
            _customer = Customer(
                first_name=customer_parse["first_name"],
                last_name=customer_parse["last_name"],

                # change date string input "dd-mm-yyyy" to date format
                date_of_birth=datetime.strptime(customer_parse["date_of_birth"],'%d-%m-%Y').date(),

                email=customer_parse["email"],
                account_customer=customer_parse["account_customer"],
                bank_transaction=customer_parse["bank_transaction"],
                credit_card=customer_parse["credit_card"],
                loan=customer_parse["loan"],
                insert_at=datetime.now(),
            )
            commit()
            result = {
                "status": 201,
                "message": "customer created !",
                # "customer": _customer.to_dict()
                # }
                "customer": {
                    "customer_id": _customer.customer_id,
                    "first_name": _customer.first_name,
                    "last_name": _customer.last_name,
                    "date_of_birth": str(_customer.date_of_birth),
                    "email": _customer.email,
                    "account_customer": _customer.account_customer,
                    "bank_transaction": _customer.bank_transaction,
                    "credit_card": _customer.credit_card,
                    "loan": _customer.loan,
                    "insert_at": str(_customer.insert_at),
                    "update_at": str(_customer.update_at),
                },
            }
            return result

        except KeyError as error:
            output = {
                "status": "Error : missing key/value of: " + str(error),
                "http status": 400,
                "customer": customer_parse,
            }
            return output

    @db_session
    def update_customer(customer_payload, customer_id):
        customer_parse = json.loads(json.dumps(customer_payload))
        try:
            customer = Customer.get_for_update(customer_id=customer_id)
            customer.first_name = customer_parse["first_name"]
            customer.last_name = customer_parse["last_name"]
            customer.date_of_birth = customer_parse["date_of_birth"]
            customer.email = customer_parse["email"]
            customer.account_customer = customer_parse["account_customer"]
            customer.bank_transaction = customer_parse["bank_transaction"]
            customer.loan = customer_parse["loan"]
            customer.update_at = datetime.now()
            commit()
            result = {
                "status": "Success",
                "message": "Success Update customer",
                "customer": {
                    "first_name": customer_parse["first_name"],
                    "last_name": customer_parse["last_name"],
                    "date_of_birth": customer_parse["date_of_birth"],
                    "email": customer_parse["email"],
                    "account_customer": customer_parse["account_customer"],
                    "bank_transaction": customer_parse["bank_transaction"],
                    "loan": customer_parse["loan"],
                    "updated_at": str(datetime.now()),
                },
            }
            return result
        except ValueError:
            result = {
                "status": str(ValueError),
                "message": "Failed Update customer",
                "customer": {
                    "first_name": customer_parse["first_name"],
                    "last_name": customer_parse["last_name"],
                    "date_of_birth": customer_parse["date_of_birth"],
                    "email": customer_parse["email"],
                    "account_customer": customer_parse["account_customer"],
                    "bank_transaction": customer_parse["bank_transaction"],
                    "loan": customer_parse["loan"],
                    "updated_at": str(datetime.now()),
                },
            }
            return result

    @db_session
    def update_customeraddress(customer_id, address_id):
        try:
            customer = Customer.get_for_update(customer_id=customer_id)
            try:
                address = Address.get_for_update(address_id=address_id)
            except TypeError:
                address.customer = customer
                address.update_at = datetime.now()
                commit()
                address_json = {
                    "street_address1": address.street_address1,
                    "street_address2": address.street_address2,
                    "city": address.city,
                    "zzicode": address.zipcode,
                    "state": address.state,
                    "country": address.country,
                    "customer": customer,
                    "updated_at": str(datetime.now()),
                }
                customer.address = address_id
                customer.update_at = datetime.now()
                commit()
            result = {
                "status": "Success",
                "message": "Success Update customer with address",
                "customer": {
                    "customer_id": customer.customer_id
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "date_of_birth": str(customer.date_of_birth),
                    "email": customer.email,
                    "account_customer": customer.account_customer,
                    "bank_transaction": customer.bank_transaction,
                    "loan": customer.loan,
                    "address": address_json
                    "updated_at": str(datetime.now()),
                },
            }
            return result
        except ValueError:
            result = {
                "status": str(ValueError),
                "message": "Failed Update customer",
                "customer": {
                    "customer_id": customer.customer_id
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "date_of_birth": str(customer.date_of_birth),
                    "email": customer.email,
                    "account_customer": customer.account_customer,
                    "bank_transaction": customer.bank_transaction,
                    "loan": customer.loan,
                    "address": address
                    "updated_at": str(datetime.now()),
                },
            }
            return result

    @db_session
    def delete_customer(customer_id):
        try:
            customer_deleted = Customer[customer_id].delete()
        except ObjectNotFound:
            result = {
                "status": 404,
                "message": "Customer with id: " + str(customer_id) + " not found"
            }
            return result
        if customer_deleted is None:
            result = {
                "status": 200,
                "message": "Customer with id: " + str(customer_id) + " Success Deleted"
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
    # print(AddressService.delete_address(1004))