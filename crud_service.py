import asyncio
import json
from datetime import datetime

from gino import Gino
from initdb import (
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

db = Gino()


class CustomerService:
    async def object_as_dict(obj):
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    async def customer_list():
        try:
            async with db.with_bind('postgres://miftah:fonez@localhost/ebanking'):

                async with db.transaction():
                    customers = []
                    async for customer in Customers.query.order_by(Customers.customer_id).gino.iterate():
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
                        await customers.append(dict_customer)
            return customers
        except ValueError:
            return str(ValueError)


asyncio.get_event_loop().run_until_complete(CustomerService.customer_list())
