from datetime import datetime, date
from pony.orm import *
from decimal import Decimal

db = Database()

# PostgreSQL
db.bind(provider='postgres', user='miftah', password='fonez', host='localhost', database='pony')



class Customer(db.Entity):
    _table_ = "customers"
    customer_id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Optional(str)
    date_of_birth = Optional(date)
    street_address = Optional(str)
    city = Optional(str)
    state = Optional(str)
    zipcode = Optional(str)
    email = Required(str)
    gender = Optional(str)
    insert_at = Required(datetime)
    update_at = Optional(datetime)


class Branches(db.Entity):
    _table_ = "branches"
    branch_id = PrimaryKey(int, auto=True)
    branch_name = Required(str)
    street_address = Optional(str)
    city = Optional(str)
    state = Optional(str)
    zipcode = Optional(str)
    phone_number = Optional(str)
    insert_at = Required(datetime)
    update_at = Optional(datetime)
    employees = Set('Employees')


class Employees(db.Entity):
    employee_id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Required(str)
    supervisor_id = Set('Employees', reverse='employee_id')
    level_of_access = Required(str)
    date_of_birth = Optional(date)
    street_address = Optional(str)
    city = Optional(str)
    state = Optional(str)
    zipcode = Optional(str)
    insert_at = Required(datetime)
    update_at = Optional(datetime)
    branches = Set('Branches')


class BranchEmployees(db.Entity):
    branches = Required('Branches', reverse='branch_id')
    employees = Required('Employees', reverse='employee_id')
    BranchEmployees_pkey = PrimaryKey(branches, employees)
    start_date = Optional(date)
    end_date = Optional(date)
    minimum_balance_restriction = Optional(Decimal)
    insert_at = Required(datetime)
    update_at = Optional(datetime)


class AccountType(db.Entity):
    account_type = PrimaryKey(str)
    minimum_balance_restriction = Optional(Decimal)
    insert_at = Required(datetime)
    update_at = Optional(datetime)


class Accounts(db.Entity):
    account_id = PrimaryKey(int, auto=True)
    account_balance = Optional(Decimal)
    branch_id = Required(Branches)
    date_opened = Optional(date)
    account_type = Required(AccountType)
    insert_at = Required(datetime)
    update_at = Optional(datetime)


class AccountCustomers(db.Entity):
    account_id = Required(Accounts)
    customer_id = Required(Customer)
    insert_at = Required(datetime)
    update_at = Optional(datetime)


class BankingTransactions(db.Entity):
    transaction_id = PrimaryKey(int, auto=True)
    maximum_limit = Required(Decimal)
    transaction_type = Required(str)
    description = Required(str)
    date = Optional(date)
    customer_id = Required(Customer)
    insert_at = Required(datetime)
    update_at = Optional(datetime)


class CreditCards(db.Entity):
    cc_number = PrimaryKey(str)
    maximum_limit = Required(Decimal)
    expiry_date = Required(date)
    credit_score = Optional(int)
    customer_id = Required(Customer)
    insert_at = Required(datetime)
    update_at = Optional(datetime)


class CCTransactions(db.Entity):
    transaction_id = PrimaryKey(str)
    cc_number = Required(CreditCards)
    transaction_date = Required(date)
    amount = Optional(Decimal)
    merchant_details = Optional(str)
    insert_at = Required(datetime)
    update_at = Optional(datetime)


class Loan(db.Entity):
    loan_id = PrimaryKey(int, auto=True)
    duration_in_years = Optional(Decimal)
    loan_start_date = Optional(date)
    interest_rate = Optional(Decimal)
    loan_amount_taken = Optional(Decimal)
    loan_amount_repaid = Optional(Decimal)
    loan_type = Optional(str)
    customer_id = Required(Customer)
    insert_at = Required(datetime)
    update_at = Optional(datetime)


sql_debug(True)
db.generate_mapping(create_tables=True)
