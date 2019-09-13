import asyncio
from gino import Gino

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(),primary_key=True)
    nickname = db.Column(db.Unicode(),default='noname')


async def migrate():
    async with db.with_bind('asyncpg://miftah:fonez@localhost/gino'):

        # Create tables
        await db.gino.create_all()

        # Create object, `id` is assigned by database
        u1 = await User.create(nickname='fantix')
        print(u1.id, u1.nickname) # 1 fantix:

        # Execute complex statement and return command status
        status, result = await User.update.values(
            nickname='No.' +db.cast(User.id, db.Unicode),
        ).where(
            User.id > 10,
        ).gino.status()
        print(status) # UPDATE 8

        # Iterate over the results of a large query in a transaction
        async with db.transaction():
            async for u in User.query.order_by(User.id).gino.iterate():
                print(u.id, u.nickname)


asyncio.get_event_loop().run_until_complete(migrate())
