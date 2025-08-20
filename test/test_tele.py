import os
import asyncio
from dotenv import load_dotenv
import aiohttp

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_test_message():
    msg = "Telegram is working! This message came from Python "
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        await session.post(url, json={
            "chat_id": CHAT_ID,
            "text": msg
        })

asyncio.run(send_test_message())
