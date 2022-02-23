import requests
import json
from config import keys

class APIEException(Exception):
    pass

class ValutConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIEException(f"Невозможно перевести одинаковые валюты {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIEException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIEException(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIEException(f"Не удалось обработать колличество {amount}")

        quote_ticker = keys[quote]
        base_ticker = keys[base]

        r = requests.get(f"https://free.currconv.com/api/v7/convert?q={quote_ticker}_{base_ticker}&compact=ultra&apiKey=e9c184ee7785b7ec0ca7")
        total = json.loads(r.content)
        list_total = str(list(total.values()))
        list_total = list_total.replace("[", "")
        list_total = list_total.replace("]", "")
        total_base = float(list_total) * float(amount)

        return total_base