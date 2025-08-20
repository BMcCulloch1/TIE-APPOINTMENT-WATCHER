import asyncio
from dotenv import load_dotenv
import sys
import os
import random

# Environment setup
# os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()


from src.pages import navigate_steps
from src.detect import detect_availability
from src.notify import send_telegram_alert
from src.storage import is_cooldown_active, save_alert_time
from playwright.async_api import async_playwright
from src.utils.stealth import stealth_async



# Load user data
NIE = os.getenv("NIE").strip()
FULL_NAME = os.getenv("FULL_NAME").strip()
COUNTRY_VALUE = os.getenv("COUNTRY_VALUE").strip()

# Run main logic
async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--no-sandbox"])

        context = await browser.new_context(
            record_har_path=os.path.join(os.path.dirname(__file__), "..", "artifacts", "debug.har"),
            user_agent=random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            ]),
            viewport=random.choice([
                {"width": 1280, "height": 720},
                {"width": 1366, "height": 768},
                {"width": 1440, "height": 900}
            ]),
            locale="es-ES",
            extra_http_headers={
                "Referer": "https://icp.administracionelectronica.gob.es/",
                "Accept-Language": "es-ES,es;q=0.9",
            }
        )

        page = await context.new_page()
        await stealth_async(page)

        try:
            await navigate_steps(page, NIE, FULL_NAME, COUNTRY_VALUE)
            status = await detect_availability(page)

            if status == "available" and not is_cooldown_active(30):
                await send_telegram_alert(
                    f"<b>TIE appointment detected</b> for {FULL_NAME} - {NIE}",
                    html_path="artifacts/result.html",
                    img_path="artifacts/result.png"
                )
                save_alert_time()
            elif status == "none":
                print("No appointments available.")
            elif status == "expired":
                print("Session expired or blocked.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await context.close()
            await browser.close()

asyncio.run(run())
