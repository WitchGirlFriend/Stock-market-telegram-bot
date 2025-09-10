import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

def get_moex_index():
    url = "https://www.moex.com/ru/index/IMOEX"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        value_div = soup.find("td", class_="values_tr_second")
        print(value_div)
        if not value_div:
            return "Не найдено"

        return value_div.text.strip()
    except Exception as e:
        return f"Ошибка: {e}"