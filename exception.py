from config import keys
import requests
import json


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_total_amount(base: str, quote: str, amount: str) -> object:
        if quote == base:
            raise APIException(f'Введите различные валюты: {base}.')

        base_ticker, quote_ticker = CryptoConverter.get_tickers(base, quote)

        try:
            amount = float(amount)
            if amount <= 0:
                raise APIException("Значение не должно быть меньше 0")
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        total_base = CryptoConverter.get_price(base_ticker, quote_ticker)
        total_amount = total_base * amount
        return total_amount

    @staticmethod
    def get_tickers(base, quote):
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        return base_ticker, quote_ticker

    @staticmethod
    def get_price(base_ticker, quote_ticker):
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        data = json.loads(r.content)
        return data.get(quote_ticker, 0)
