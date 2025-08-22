from dotenv import load_dotenv
import os 
import time
import random, asyncio


# Make sure artifacts folder exists
os.makedirs("artifacts", exist_ok=True)

load_dotenv()
NIE = os.getenv("NIE").strip()
FULL_NAME = os.getenv("FULL_NAME").strip()
COUNTRY_VALUE = os.getenv("COUNTRY_VALUE").strip()


async def navigate_steps(page, nie, full_name, country_value):
    async def jitter(min_ms=2000, max_ms=4000):
        await asyncio.sleep(random.uniform(min_ms/1000, max_ms/1000))

    # === STEP 1: Province Selection ===
    await page.goto("https://icp.administracionelectronica.gob.es/icpplus/index.html", timeout=60000)
    await jitter()

    # ✅ Hover and simulate user interaction
    await page.hover("select[name='form']")
    await page.mouse.move(200, 200)
    await page.mouse.click(200, 200)
    await jitter()

    await page.select_option("select[name='form']", label="Lleida")
    await jitter()
    await page.click("#btnAceptar")


    # === STEP 2: Office Selection ===
    await page.wait_for_selector("select[name='sede']")
    await jitter()
    await page.select_option("select[name='sede']", label="CNP LLEIDA, DE L`ENSENYANÇA, 2, LLEIDA")
    await jitter()

    # === STEP 3: Appointment Type ===
    await page.select_option("select[name='tramiteGrupo[0]']", value="4010")
    await jitter()
    await page.click("#btnAceptar")


    # === STEP 4: Sin Cl@ve Login ===
    btn_sin_clave = page.locator("#btnEntrar")
    await btn_sin_clave.wait_for(state="visible", timeout=10000)
    await jitter()
    await btn_sin_clave.hover()
    await btn_sin_clave.click()


    # === STEP 5: User Details ===
    await page.click("input[name='txtIdCitado']")
    await page.keyboard.type(nie, delay=120)
    await jitter()

    await page.click("input[name='txtDesCitado']")
    await page.keyboard.type(full_name, delay=120)
    await jitter()

    await page.select_option("select[name='txtPaisNac']", value=country_value)
    await jitter()

    # Log for debug
    print("▶ Country value selected:", await page.input_value('select[name="txtPaisNac"]'))

    # Acceptar
    btn_enviar = page.locator("input#btnEnviar")
    await btn_enviar.wait_for(state="visible", timeout=10000)
    await jitter()
    await btn_enviar.hover()
    await btn_enviar.click()

    # === STEP 6: Solicitar Cita ===
    # Wait for the container with the Solicitar Cita buttons to appear
    await page.wait_for_selector("div.fld.layout--abajo", timeout=10000)
    await jitter()

    # Then target the second #btnEnviar (Solicitar Cita)
    btn_solicitar_cita = page.locator('//input[@id="btnEnviar" and @value="Solicitar Cita"]')
    await btn_solicitar_cita.wait_for(state="visible", timeout=10000)
    await jitter()
    await btn_solicitar_cita.hover()
    await btn_solicitar_cita.click()



    # Wait for network idle
    await page.wait_for_load_state("networkidle")
