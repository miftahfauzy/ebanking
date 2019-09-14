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
    # def object_as_dict(obj):
    #     return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    def customer_list():
        try:
            with db.with_bind('postgres://miftah:fonez@localhost/ebanking'):

                with db.transaction():
                    customers = []
                    for customer in Customers.query.order_by(Customers.customer_id).gino.iterate():
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
        except ValueError:
            return str(ValueError)


CustomerService.customer_list()
