import requests
from bs4 import BeautifulSoup


def get_currency_rates():
    url = "https://www.cbr.ru/currency_base/daily/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", class_="data")  # таблица с курсами

        currencies = {"USD": None, "EUR": None, "JPY": None}

        for row in table.find_all("tr")[1:]:  # пропускаем заголовок
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            char_code = cols[1].text.strip()
            value = cols[4].text.strip().replace(",", ".")

            if char_code in currencies:
                currencies[char_code] = float(value)

        return currencies

    except Exception as e:
        return {"USD": f"Ошибка: {e}", "EUR": "—", "JPY": "—"}