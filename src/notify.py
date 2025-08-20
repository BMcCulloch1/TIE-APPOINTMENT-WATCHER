import os
import asyncio
from dotenv import load_dotenv
import aiohttp

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_alert(msg, html_path = None, img_path = None):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print ("Telegram not configured properly")
        return
    
    async with aiohttp.ClientSession() as session: 
        #Send a text message
        await session.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "html"
        })

        #Send a screenshot
        if img_path:
            with open(img_path, 'rb') as f:
                await session.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                    data = {"chat_id": CHAT_ID,},
                    files = {"photo":f}
                )

