from tie_selectors import NO_CITAS_TEXT, SESION_CADUCADA_TEXTS

async def detect_availability(page) -> str:
    html = await page.content()
    text = html.lower()

    if any(expired in text for expired in SESION_CADUCADA_TEXTS):
        return "expired"
    
    if NO_CITAS_TEXT in text:
        return "none"
    
    return "available"