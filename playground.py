from datetime import date
from datetime import datetime
from decimal import Decimal
from pony.orm import *

db = Database()

# PostgreSQL
db.bind(
    provider="postgres",
    user="miftah",
    password="fonez",
    host="localhost",
    database="playground",
)


class Customer(db.Entity):
    customer_id = PrimaryKey(int, auto=True)
    first_name = Optional(str, 45)
    last_name = Optional(str, 45)
    date_of_birth = Optional(date)
    email = Optional(str, 55)
    address = Set("Address")
    insert_at = Optional(datetime)
    update_at = Optional(datetime)


class Address(db.Entity):
    address_id = PrimaryKey(int, auto=True)
    street_address1 = Optional(str)
    street_address2 = Optional(str)
    city = Optional(str, 45)
    zipcode = Optional(str, 25)
    state = Optional(str, 45)
    country = Optional(str, 45)
    insert_at = Optional(datetime)
    update_at = Optional(datetime)
    customers = Optional(Customer)


sql_debug(True)
db.generate_mapping(create_tables=True)


@db_session()
def create_custaddr():    
    customer = Customer(
        first_name="Miftah",
        last_name="Fauzy",
        date_of_birth=datetime.strptime("22051968", "%d%m%Y").date(),
        email='miftah.fauzy@gmail.com',
        insert_at=datetime.now()
    )
    d1 = Address(
        street_address1='Jl. Cibolerang',
        street_address2='No.75',
        city='Bandung',
        zipcode='21141',
        state='Jawa Barat',
        country='Indonesia',
        insert_at=datetime.now(),
        customers=customer
    )

    commit()


if __name__ == "__main__":
    create_custaddr()