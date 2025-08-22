import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
import asyncio
import json

load_dotenv()

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,  # no need to open browser UI for JSON
            proxy={
                "server": f"http://{os.getenv('WEBSHARE_PROXY_HOST')}:{os.getenv('WEBSHARE_PROXY_PORT')}",
                "username": os.getenv("WEBSHARE_PROXY_USER"),
                "password": os.getenv("WEBSHARE_PROXY_PASS"),
            },
            args=["--no-sandbox"]
        )

        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to JSON API and get IP info
        await page.goto("https://ipinfo.io/json")
        content = await page.content()
        json_text = await page.inner_text("body")
        data = json.loads(json_text)

        print("✅ Proxy Test Result:")
        print(f"IP Address: {data.get('ip')}")
        print(f"City: {data.get('city')}")
        print(f"Region: {data.get('region')}")
        print(f"Country: {data.get('country')} 🇪🇸" if data.get("country") == "ES" else f"Country: {data.get('country')} ❌ Not Spain")

        await browser.close()

asyncio.run(run())
