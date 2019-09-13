import asyncio
from gino import Gino

db = Gino()


class Customer(db.Model):
    __tablename__ = "customer"

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
    street_address = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(25), nullable=True)
    state = db.Column(db.String(3), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    phone_number = db.Column(db.String(12), nullable=True)
    insert_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)


async def migrate():
    await db.set_bind('postgres://miftah:fonez@localhost/ebanking')
    await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(migrate())
