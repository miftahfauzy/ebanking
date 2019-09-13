import asyncio
from gino import Gino

db = Gino()


class Customers(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=True)
    last_name = db.Column(db.String(45), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    street_address = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(25), nullable=True)
    state = db.Column(db.String(3), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(45), nullable=True)
    gender = db.Column(db.String(1), nullable=True)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


class Branches(db.Model):
    __tablename__ = "branches"
    branch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_name = db.Column(db.String(45), nullable=True)
    street_address = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(25), nullable=True)
    state = db.Column(db.String(3), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    phone_number = db.Column(db.String(12), nullable=True)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


class Employees(db.Model):
    __tablename__ = "employees"
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=True)
    last_name = db.Column(db.String(45), nullable=True)
    supervisor_id = db.Column(db.Integer, db.ForegnKey('employees.employee_id'), nullable=False)
    level_of_access = db.Column(db.String(15), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    street_address = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(25), nullable=True)
    state = db.Column(db.String(3), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


class BranchEmployees(db.Model):
    __tablename__ = "branch_employees"

    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    minimum_balance_restriction = db.Column(db.Number, nullable=True)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


class AccountType(db.Model):
    __tablename__ = "account_type"

    account_type = db.Column(db.String(20), primary_key=True)
    minimum_balance_restriction = db.Column(db.Number, nullable=True)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


class Accounts(db.Model):
    __tablename__ = "accounts"

    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_balance = db.Column(db.Numeric, nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=True)
    date_opened = db.Column(db.Date, nullable=True)
    account_type = db.Column(db.String(20), db.ForeignKey('account_type.account_type'), nullable=True)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


class AccountCustomers(db.Model):
    __tablename__ = "account_customers"

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


class BankingTransactions(db.Model):
    __tablename__ = "banking_transactions"

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maximum_limit = db.Column(db.Numeric, nullable=True)
    transaction_type = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(45), nullable=True)
    date = db.Column(db.Date, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


class CreditCards(db.Model):
    __tablename__ = "credit_cards"

    cc_numbers = db.Column(db.String(20), primary_key=True, nullable=False)
    maximum_limit = db.Column(db.Numeric, nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    credit_score = db.Column(db.Integer, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


async def migrate():
    await db.set_bind('postgres://miftah:fonez@localhost/ebanking')
    await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(migrate())
