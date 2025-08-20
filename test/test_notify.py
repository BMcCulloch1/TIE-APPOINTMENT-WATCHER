import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.notify import send_telegram_alert

async def test():
    await send_telegram_alert("This is a test alert from notify.py!")

asyncio.run(test())
