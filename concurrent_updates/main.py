import asyncio
import datetime
import random

from concurrent_updates.postgres_threaded_connection_pool import PGConnectionPoolFactory

MIN_IDS = 1
MAX_IDS = 1000000
MAX_PARALLEL_TASKS = 150
CURRENCIES = ['USD', 'AUD', 'JPY']
REGIONS = ['US', 'PL', 'AE']


async def prepare_table(connection_pool):
    async with connection_pool.connection() as conn:
        create_table = """
            create table if not exists account (
                id bigint primary key,
                user_id bigint,
                currency varchar(10),
                region varchar(10),
                balance decimal,
                last_updated_at timestamp
            );
        """
        await conn.execute(create_table)


async def prepare_index(connection_pool):
    async with connection_pool.connection() as conn:
        create_index = """
            create index if not exists multicolumn_index on account (user_id, region)
        """
        await conn.execute(create_index)


async def truncate_account_table(connection_pool):
    async with connection_pool.connection() as conn:
        sql = "truncate table account"
        await conn.execute(sql)


async def create_accounts(connection_pool, from_id, to_id):
    user_id = random.randint(MIN_IDS, MAX_IDS)
    currency = CURRENCIES[random.randint(0, len(CURRENCIES) - 1)]
    region = REGIONS[random.randint(0, len(REGIONS) - 1)]
    balance = random.randint(0, 1000)
    for i in range(from_id, to_id):
        await create_account(
            connection_pool=connection_pool,
            id=i,
            user_id=user_id,
            currency=currency,
            region=region,
            balance=balance,
            last_updated_at=datetime.datetime.now()
        )


async def create_account(connection_pool, id, user_id, currency, region, balance, last_updated_at):
    async with connection_pool.connection() as conn:
        data = (id, user_id, currency, region, balance, last_updated_at)
        await conn.execute(
            """
                insert into account (id, user_id, currency, region, balance, last_updated_at) 
                values (%s, %s, %s, %s, %s, %s)
            """,
            data
        )
        print("created row")


async def update_transfer(connectionpool, account_id, balance):
    async with connectionpool.connection() as conn:
        await conn.execute(
            """
                update account set balance = %s, last_updated_at = %s where id = %s
            """,
            (balance, datetime.datetime.now(), account_id)
        )
    # print("updated row")


async def main(loop, generate_data):
    async with PGConnectionPoolFactory().create() as connection_pool:
        await prepare_table(connection_pool)
        print("prepared table")
        await prepare_index(connection_pool)
        print("prepared index")
        if generate_data:
            await truncate_account_table(connection_pool)
            print("cleaned table")

            generated_ids = [i for i in range(MIN_IDS, MAX_IDS)]
            chunk_size = 100
            coroutines = []
            for i in range(0, len(generated_ids), chunk_size):
                coroutines.append(create_accounts(connection_pool, i, i + chunk_size))
            tasks = [loop.create_task(i) for i in coroutines]
            await asyncio.gather(*tasks)
            print("generated data")
        else:
            print("will not clean up data and regenerate.")
        while True:
            account_id = random.randint(MIN_IDS, MAX_IDS)
            balance = random.randint(0, 1000)
            coroutines = []
            for i in range(0, MAX_PARALLEL_TASKS):
                coroutines.append(update_transfer(connection_pool, account_id, balance))
            tasks = [loop.create_task(i) for i in coroutines]
            await asyncio.gather(*tasks)


loop = asyncio.new_event_loop()
loop.create_task(main(loop, False))
loop.run_forever()
