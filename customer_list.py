import asyncio
from gino import Gino
from initdb import Customers

db = Gino()


async def migrate():
    async with db.with_bind('asyncpg://miftah:fonez@localhost/ebanking'):

        # Iterate over the results of a large query in a transaction
        async with db.transaction():
            async for customers in Customers.query.order_by(Customers.id).gino.iterate():
                print(customers.customer_id, customers.first_name, customers.last_name, customers.date_of_birth)


asyncio.get_event_loop().run_until_complete(migrate())
