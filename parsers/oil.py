import asyncio
from playwright.async_api import async_playwright
import os

async def get_oil_prices():
    results = await asyncio.gather(
        get_brent_price(),
        get_crude_price()
    )
    return results

async def get_brent_price():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        if os.path.exists("state.json"):
            context = await browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    viewport={"width": 1280, "height": 720},
    java_script_enabled=True,
    locale="ru-RU"
)
        else:
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto("https://ru.investing.com/commodities/brent-oil", timeout=30000)
            input("🧩 Пройди капчу в браузере и нажми Enter здесь...")
            await context.storage_state(path="state.json")
            await browser.close()
            return "Сессия сохранена. Запусти скрипт снова."
        page = await context.new_page()

        try:
            context = await browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    viewport={"width": 1280, "height": 720},
    java_script_enabled=True,
    locale="ru-RU"
)
            page = await context.new_page()
            await page.goto("https://ru.investing.com/commodities/brent-oil", timeout=30000)
            await context.storage_state(path="state.json")
            # Ждём, пока появится нужный элемент
            await page.wait_for_selector("div[data-test='instrument-price-last']", timeout=15000)
            element = await page.query_selector("div[data-test='instrument-price-last']")
            price = await element.text_content()
            return price.strip()
        except Exception as e:
            return f"Ошибка: {e}"
        finally:
            await browser.close()

async def get_crude_price():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # можно False для отладки
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
        )
        page = await context.new_page()

        try:
            await page.goto("https://ru.investing.com/commodities/crude-oil", timeout=30000)
            # Ждём, пока появится нужный элемент
            await page.wait_for_selector("div[data-test='instrument-price-last']", timeout=15000)
            element = await page.query_selector("div[data-test='instrument-price-last']")
            price = await element.text_content()
            return price.strip()
        except Exception as e:
            return f"Ошибка: {e}"
        finally:
            await browser.close()
