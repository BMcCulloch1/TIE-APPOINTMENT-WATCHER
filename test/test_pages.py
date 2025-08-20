import asyncio
from dotenv import load_dotenv
import sys
import os
import random  


os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages import navigate_steps
from playwright.async_api import async_playwright
from utils.stealth import stealth_async

load_dotenv()

NIE = os.getenv("NIE").strip()
FULL_NAME = os.getenv("FULL_NAME").strip()
COUNTRY_VALUE = os.getenv("COUNTRY_VALUE").strip()


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox"]
        )


        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        ]

        VIEWPORTS = [
            {"width": 1280, "height": 720},
            {"width": 1366, "height": 768},
            {"width": 1440, "height": 900},
        ]

        context = await browser.new_context(
            record_har_path="artifacts/debug.har",
            user_agent=random.choice(USER_AGENTS),
            viewport=random.choice(VIEWPORTS),
            locale="es-ES",
            extra_http_headers={
                "Referer": "https://icp.administracionelectronica.gob.es/",
                "Accept-Language": "es-ES,es;q=0.9",
            }
        )

        page = await context.new_page()

        # Apply stealth before any action
        await stealth_async(page)

        # Navigate
        await navigate_steps(page, NIE, FULL_NAME, COUNTRY_VALUE)

        # Save storage state if you want (optional)
        await context.storage_state(path="auth.json")

        # Let it sit to observe
        await page.wait_for_timeout(10000)

        await context.close()
        await browser.close()

asyncio.run(run())
