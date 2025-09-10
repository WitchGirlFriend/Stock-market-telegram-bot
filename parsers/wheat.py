from playwright.async_api import async_playwright

async def get_wheat_price():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # для отладки
        context = await browser.new_context(storage_state="state.json")
        page = await context.new_page()

        try:
            await page.goto("https://ru.investing.com/commodities/us-wheat", timeout=30000)
            await page.wait_for_selector("div[data-test='instrument-price-last']", timeout=15000)
            element = await page.query_selector("div[data-test='instrument-price-last']")
            price = await element.text_content()
            return price.strip()
        except Exception as e:
            return f"Ошибка: {e}"
        finally:
            await browser.close()