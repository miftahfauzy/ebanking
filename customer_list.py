import asyncio
import json
import pprint
from initdb import db, Customers


class CustomerService:
    async def customer_list():
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

    # async def get_customer(_customer_id):
    #     async with db.with_bind("postgresql://miftah:fonez@localhost/ebanking"):
    #
    #         customer = await Customers.get(_customer_id)
    #         print(customer.customer_id, customer.first_name)
    #
    #         dict_customer = {
    #             "customer_id": customer.customer_id,
    #             "first_name": customer.first_name,
    #             "last_name": customer.last_name,
    #             "date_of_birth": customer.date_of_birth,
    #             "street_address": customer.street_address,
    #             "city": customer.city,
    #             "state": customer.state,
    #             "zipcode": customer.zipcode,
    #             "email": customer.email,
    #             "gender": customer.gender,
    #             "insert_at": customer.insert_at,
    #             "update_at": customer.update_at,
    #         }
    #         await db.pop_bind().close()
    #         return dict_customer


customers_dict = asyncio.get_event_loop().run_until_complete(CustomerService.customer_list())
pp = pprint.PrettyPrinter(width=41, compact=True)
pp.pprint(customers_dict)
# print(customers_dict)


# customer_id = 151
# print(
#     asyncio.get_event_loop().run_until_complete(
#         CustomerService.get_customer(customer_id)
#     )
# )
