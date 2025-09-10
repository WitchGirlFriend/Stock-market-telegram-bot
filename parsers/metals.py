import requests
from bs4 import BeautifulSoup

def get_metal_price(url: str, metal_id: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        price_span = soup.find("span", id=metal_id)
        if price_span:
            return price_span.text.strip().replace(",", "")
        return "Не найдено"
    except Exception as e:
        return f"Ошибка: {e}"

def get_metal_prices() -> dict:
    return {
        "Gold": get_metal_price("https://www.kitco.com/gold-price-today-usa/", "sp-bid"),
        "Silver": get_metal_price("https://www.kitco.com/silver-price-today-usa/", "sp-bid"),
        "Platinum": get_metal_price("https://www.kitco.com/platinum-price-today-usa/", "sp-bid")
    }