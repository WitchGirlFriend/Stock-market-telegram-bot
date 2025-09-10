from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import send_or_update
import asyncio

scheduler = AsyncIOScheduler()
scheduler.add_job(send_or_update, "interval", minutes=1)
scheduler.start()

async def main():
    while True:
        await asyncio.sleep(1)

asyncio.run(main())