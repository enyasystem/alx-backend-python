import asyncio
import aiosqlite
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'users.db'

async def async_fetch_users():
    async with aiosqlite.connect(str(DB_PATH)) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            rows = await cursor.fetchall()
            return rows

async def async_fetch_older_users():
    async with aiosqlite.connect(str(DB_PATH)) as db:
        async with db.execute('SELECT * FROM users WHERE age > ?', (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows

async def fetch_concurrently():
    results = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    all_users, older_users = results
    print('All users count:', len(all_users))
    print('Older users count:', len(older_users))

if __name__ == '__main__':
    asyncio.run(fetch_concurrently())
