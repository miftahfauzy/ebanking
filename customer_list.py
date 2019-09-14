import asyncio
import asyncpg
from initdb import db, Customers


class CustomerService:
    async with db.with_bind('asyncpg://miftah:fonez@localhost/ebanking'):
        async def customer_list():

            async with db.transaction():

                customers = []

                # Iterate over the results of a large query in a transaction
                async for customer in Customers.query.order_by(Customers.customer_id).gino.iterate():
                    # print(customers.customer_id, customers.first_name, customers.last_name, customers.date_of_birth)
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
                        "update_at": customer.update_at
                    }
                    customers.append(dict_customer)
                return customers

    async def get_customer(_customer_id):

        conn = await asyncpg.connect('postgresql://miftah:fonez@localhost/gino')
        customer = await Customers.get(conn, _customer_id)
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
            "update_at": customer.update_at
        }
        return dict_customer

# print(asyncio.get_event_loop().run_until_complete(CustomerService.customer_list()))


customer_id = 151
print(asyncio.get_event_loop().run_until_complete(CustomerService.get_customer(customer_id)))
