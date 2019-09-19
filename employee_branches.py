
from datetime import date
from datetime import datetime
from decimal import Decimal
from pony.orm import *


db = Database()

# PostgreSQL
db.bind(provider='postgres', user='miftah', password='fonez', host='localhost', database='pony')


class Branches(db.Entity):
    branch_id = PrimaryKey(int, auto=True)
    branch_name = Optional(str, 45)
    phone_number = Optional(str, 12)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    branches_employeess = Set('Branches_employees')
    accounts = Set('Account')
    bank_transaction = Required('Bank_transaction')


class Branches_employees(db.Entity):
    id = PrimaryKey(int, auto=True)
    branches = Required(Branches)
    start_date = Optional(date)
    end_date = Optional(date)
    minimum_balance_restriction = Optional(Decimal)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    employee = Required('Employee')


class Account_type(db.Entity):
    account_type = PrimaryKey(str, 20, auto=True)
    minimum_balance_restriction = Optional(Decimal)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    accounts = Set('Account')


class Account(db.Entity):
    account_id = PrimaryKey(int, auto=True)
    account_balance = Optional(Decimal)
    branches = Required(Branches)
    date_opened = Optional(date)
    account_type = Required(Account_type)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    account_customer = Required('Account_customer')


class Employee(db.Entity):
    employee_id = PrimaryKey(int, auto=True)
    employees = Set('Employee', reverse='supervisor_id')
    level_of_access = Optional(str, 15)
    supervisor_id = Required('Employee', reverse='employees')
    branches_employeess = Set(Branches_employees)
    first_name = Optional(str, 45)
    last_name = Optional(str, 45)
    birth_of_date = Optional(date)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    address = Required('Address')


class Customer(db.Entity):
    customer_id = PrimaryKey(int, auto=True)
    first_name = Optional(str, 45)
    last_name = Optional(str, 45)
    date_of_birth = Optional(date)
    email = Optional(str, 55)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    account_customer = Required('Account_customer')
    bank_transaction = Required('Bank_transaction')
    credit_card = Required('Credit_card')
    loan = Required('Loan')
    address = Required('Address')


class Account_customer(db.Entity):
    accounts = Set(Account)
    customers = Set(Customer)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)


class Bank_transaction(db.Entity):
    transaction_id = PrimaryKey(int, auto=True)
    maximum_limit = Optional(Decimal)
    description = Optional(str)
    transaction_date = Optional(datetime)
    customers = Set(Customer)
    branchess = Set(Branches)
    transaction_types = Required('Transaction_types')


class Credit_card(db.Entity):
    cc_nmber = PrimaryKey(str, 20, auto=True)
    maximum_limit = Optional(Decimal, precision=2)
    expiry_date = Optional(date)
    credit_score = Optional(int)
    customers = Set(Customer)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    cc_transaction = Required('Cc_transaction')


class Cc_transaction(db.Entity):
    transaction_id = PrimaryKey(int, auto=True)
    credit_cards = Set(Credit_card)
    transaction_date = Optional(datetime)
    amount = Optional(Decimal, precision=2)
    merchant_details = Optional(str, 100)
    insert_date = Optional(datetime)
    update_date = Optional(datetime)


class Loan(db.Entity):
    loan_id = PrimaryKey(int, auto=True)
    duration_in_years = Optional(int)
    loan_start_date = Optional(date)
    interest_rate = Optional(float)
    loan_amount_taken = Optional(Decimal, precision=2)
    loan_amount_repaid = Optional(Decimal, precision=2)
    loan_type = Optional(str, 45)
    customers = Set(Customer)
    inset_at = Optional(datetime)
    update_at = Optional(datetime)


class Address(db.Entity):
    address_id = PrimaryKey(int, auto=True)
    street_address1 = Optional(str)
    street_address2 = Optional(str)
    city = Optional(str, 25)
    zipcode = Optional(str, 15)
    state = Optional(str, 45)
    country = Optional(str, 45)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    employees = Set(Employee)
    customers = Set(Customer)


class Transaction_types(db.Entity):
    transaction_type_code = PrimaryKey(str, 25, auto=True)
    transaction_type_description = Optional(str)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    bank_transactions = Set(Bank_transaction)


sql_debug(True)
db.generate_mapping(create_tables=True)
