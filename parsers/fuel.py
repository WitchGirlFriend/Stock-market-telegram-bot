import requests
from bs4 import BeautifulSoup

def get_fuel_prices():
    url = 'https://fuelprices.ru/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        fuel_data = {}

        # Дизель
        diesel_card = soup.find('div', class_='fuel-card border-diesel')
        if diesel_card:
            price_div = diesel_card.find('div', class_='price')
            if price_div:
                price = price_div.get_text(strip=True)
                fuel_data['Дизель'] = price

        # Для бензина АИ-92
        ai92_card = soup.find('div', class_='fuel-card border-ai80')
        if ai92_card:
            price_div = ai92_card.find('div', class_='price')
            if price_div:
                price = price_div.get_text(strip=True)
                fuel_data['АИ-92'] = price

        # Для бензина АИ-95
        ai95_card = soup.find('div', class_='fuel-card border-ai92')
        if ai95_card:
            price_div = ai95_card.find('div', class_='price')
            if price_div:
                price = price_div.get_text(strip=True)
                fuel_data['АИ-95'] = price

        # АИ-98
        ai98_card = soup.find('div', class_='fuel-card border-ai95')
        if ai98_card:
            price_div = ai98_card.find('div', class_='price')
            if price_div:
                price = price_div.get_text(strip=True)
                fuel_data['АИ-98'] = price
        return fuel_data

    except Exception as e:
        return {"Ошибка": str(e)}
