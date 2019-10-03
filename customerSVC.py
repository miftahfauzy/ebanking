from __future__ import absolute_import, print_function
import json
from decimal import Decimal
from datetime import datetime

from pony.converting import str2datetime
from pony.orm import *

from initdb_estore import *


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
                "address": customer[11]
            }
            arr_customer.append(json_customer)
        return arr_customer

    @db_session
    def get_customerbyid(cust_id):
        customer = Customer.get(customer_id=cust_id)
        if customer is None:
            result = {
                "status": 401,
                "message": "customer with id: " + str(cust_id) + " not found"
            }
            return result
        result = {
            "status": 200,
            "message": "customer found",
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
                "update_at": str(customer.update_at)
            }
        }
        return result


class AddressService:

    @db_session
    def address_list():
        arr_address = []
        addresses = select(
            (a.address_id, a.street_address1, a.street_address2, a.city, a.zipcode, a.state, a.country, a.insert_at, a.update_at)
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
                "update_at": str(addr[8])
            }
            arr_address.append(json_address)
        return arr_address

    @db_session
    def get_addressbyid(addr_id):
        address = Address.get(address_id=addr_id)
        if address is None:
            result = {
                "status": 401,
                "message": "Address with id: " + str(addr_id) + " not found"
            }
            return result
        result = {
            "status": 200,
            "message": "address found !",
            "address": {
                "address_id": address.address_id,
                "street_address1": address.street_address1,
                "street_address2": address.street_address2,
                "city": address.city,
                "zipcode": address.zipcode,
                "state": address.state,
                "country": address.country,
                "insert_at": str(address.insert_at),
                "update_at": str(address.update_at)
            }
        }

        return result

    @db_session
    def create_address(address_payload):
        address_parse = json.loads(json.dumps(address_payload))



# if __name__ == "__main__":
    # print(CustomerService.customer_list())
    # print(CustomerService.get_customerbyid(1))
    # print(CustomerService.get_addressbyid(1))
# print(CustomerService.address_list())
