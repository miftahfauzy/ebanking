import asyncio
import json
import pprint
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from zope.sqlalchemy import ZopeTransactionExtension

from initdb import (
    db,
    Customers,
    Branches,
    Employees,
    BranchEmployees,
    AccountType,
    Accounts,
    AccountCustomers,
    BankingTransactions,
    CreditCards,
    CCTransactions,
    Loan
)

class CustomerService:
    def customer_list():
        await db.set_bind("postgresql://miftah:fonez@localhost/ebanking")

        _customers = await Customers.query.gino.all()
        customers = []
        # print(customers.customer_id, customers.first_name, customers.last_name, customers.date_of_birth)
        for customer in _customers:
            dict_customer = {
                "customer_id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "date_of_birth": customer.date_of_birth,
                "street_address": customer.street_address,
                "city": customer.city,
                "state": customer.state,
                "zipcode": customer.zipcode,
                "email": customer.email,
                "gender": customer.gender,
                "insert_at": customer.insert_at,
                "update_at": customer.update_at,
            }
            customers.append(dict_customer)
        await db.pop_bind().close()
        return customers

    async def get_customer(_customer_id):
        await db.set_bind("postgresql://miftah:fonez@localhost/ebanking")

        customer = await Customers.get(_customer_id)
        # print(customer.customer_id, customer.first_name)

        dict_customer = {
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "date_of_birth": customer.date_of_birth,
            "street_address": customer.street_address,
            "city": customer.city,
            "state": customer.state,
            "zipcode": customer.zipcode,
            "email": customer.email,
            "gender": customer.gender,
            "insert_at": customer.insert_at,
            "update_at": customer.update_at,
        }
        await db.pop_bind().close()
        return dict_customer

    async def update_customer(_customer_id, upd_customer):
        await db.set_bind("postgresql://miftah:fonez@localhost/ebanking")

        customer_parse = json.loads((json.dumps(upd_customer)))

        # # get its customer
        # mcustomer_id = await Customers.select('customer_id').where(
        #     Customers.customer_id == _customer_id).gino.scalar()
        # assert mcustomer_id == Customers.customer_id  # they are both 'the same' before the update
        #
        # # modification here
        # await Customers.update(
        #     # customer_id=customer_parse['customer_id'],
        #     first_name=customer_parse['first_name'],
        #     last_name=customer_parse['last_name'],
        #     date_of_birth=customer_parse['date_of_birth'],
        #     street_address=customer_parse['street_address'],
        #     city=customer_parse['city'],
        #     state=customer_parse['state'],
        #     zipcode=customer_parse['zipcode'],
        #     email=customer_parse['email'],
        #     gender=customer_parse['gender'],
        #     insert_at=customer_parse['insert_at'],
        #     update_at=datetime.now()
        # ).apply()

        # Execute complex statement and return command status
        status, result = await Customers.update.values(
            first_name=customer_parse['first_name'],
            last_name=customer_parse['last_name'],
            date_of_birth=datetime.strptime(customer_parse['date_of_birth'], "%d%m%Y").date(),
            street_address=customer_parse['street_address'],
            city=customer_parse['city'],
            state=customer_parse['state'],
            zipcode=customer_parse['zipcode'],
            email=customer_parse['email'],
            gender=customer_parse['gender'],
            update_at=datetime.now()
        ).where(
            Customers.customer_id == _customer_id,
        ).gino.status()

        if int(status[-1]) > 0:
            result_customer = {
                "status:": "Success " + status,
                "customer": {
                    "customer_id": _customer_id,
                    "first_name": customer_parse['first_name'],
                    "last_name": customer_parse['last_name'],
                    "date_of_birth": customer_parse['date_of_birth'],
                    "street_address": customer_parse['street_address'],
                    "city": customer_parse['city'],
                    "state": customer_parse['state'],
                    "zipcode": customer_parse['zipcode'],
                    "email": customer_parse['email'],
                    "gender": customer_parse['gender'],
                    "update_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                }
            }
            await db.pop_bind().close()
            return result_customer
        else:
            result_customer = {
                "status:": "Failed customer ID: " + str(_customer_id) + ', not found!',
                "customer": {
                    "customer_id": _customer_id,
                    "first_name": customer_parse['first_name'],
                    "last_name": customer_parse['last_name'],
                    "date_of_birth": customer_parse['date_of_birth'],
                    "street_address": customer_parse['street_address'],
                    "city": customer_parse['city'],
                    "state": customer_parse['state'],
                    "zipcode": customer_parse['zipcode'],
                    "email": customer_parse['email'],
                    "gender": customer_parse['gender'],
                    "update_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                }
            }
            await db.pop_bind().close()
            return result_customer

    async def create_customer(json_customer):
        await db.set_bind("postgresql://miftah:fonez@localhost/ebanking")
        try:
            customer_parse = json.loads((json.dumps(json_customer)))

            customer = await Customers.create(
                first_name=customer_parse['first_name'],
                last_name=customer_parse['last_name'],
                date_of_birth=datetime.strptime(customer_parse['date_of_birth'], "%d%m%Y").date(),
                street_address=customer_parse['street_address'],
                city=customer_parse['city'],
                state=customer_parse['state'],
                zipcode=customer_parse['zipcode'],
                email=customer_parse['email'],
                gender=customer_parse['gender'],
                insert_at=datetime.now()
            )
            response_payload = {
                "response": {
                    "status": 'Success',
                    "customer": json_customer
                }
            }
            await db.pop_bind().close()
            return response_payload

        except ValueError:
            response_payload = {
                "response": {
                    "status": 'Failed ' + str(ValueError),
                    "customer": json_customer
                }
            }
            await db.pop_bind().close()
            return response_payload

    async def delete_customer(_customer_id):
        await db.set_bind("postgresql://miftah:fonez@localhost/ebanking")

        status, result = await Customers.delete.where(Customers.customer_id == _customer_id).gino.status()
        response_payload = {
            "status": status,
            "result": result
        }
        await db.pop_bind().close()
        return response_payload




# test all the function
# -------------------------------------------------------------------------------
# Customer List
# customers_dict = asyncio.get_event_loop().run_until_complete(CustomerService.customer_list())
# pp = pprint.PrettyPrinter(width=41, compact=True)
# pp.pprint(customers_dict)
# print(customers_dict)

# Get Customer by Customer ID
# customer = asyncio.get_event_loop().run_until_complete(CustomerService.get_customer(customer_id))

customer_id = 200
# bod = datetime.strptime('22051968', "%d%m%Y").date()
# customer_json = {
#     "first_name": 'Miftah',
#     "last_name": 'Fauzy',
#     "date_of_birth": '22051968',
#     "street_address": 'jl. Kel. Margahayu IV No.7',
#     "city": 'Kota Bekasi',
#     "state": 'Bekasi',
#     "zipcode": 17113,
#     "email": 'miftahfauzy@outlook.com',
#     "gender": 'L'
# }

# Update Customer by Customer ID
# customer = asyncio.get_event_loop().run_until_complete(CustomerService.update_customer(customer_id, customer_json))

# Create Customer
json_customer = {
    "first_name": 'Miftah',
    "last_name": 'Fauzy',
    "date_of_birth": '22051968',
    "street_address": 'jl. Kel. Margahayu IV No.7',
    "city": 'Kota Bekasi',
    "state": 'Bekasi',
    "zipcode": 17113,
    "email": 'miftahfauzy@outlook.com',
    "gender": 'L',
    "insert_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
    "update_at": None
}
# result = asyncio.get_event_loop().run_until_complete(CustomerService.create_customer(json_customer))
# Delete Customer by Customer ID
# result = asyncio.get_event_loop().run_until_complete(CustomerService.delete_customer(customer_id))
# print(result)


# pp = pprint.PrettyPrinter(width=40, compact=True)
# pp.pprint(customer)

