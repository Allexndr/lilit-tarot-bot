import asyncio
from bot.database import init_db, close_db

async def run_update():
    print("Initializing database tables...")
    await init_db()
    print("Database tables initialized successfully.")
    await close_db()

if __name__ == "__main__":
    asyncio.run(run_update())
