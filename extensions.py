import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'f"Валюта {quote} не найдена!"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'f"Валюта {base} не найдена!"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        resp = json.loads(r.content)
        total_base = json.loads(r.content)[keys[base]] * float(amount)

        return total_base

