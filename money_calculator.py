"""Simple money expressions calculator"""

from functools import lru_cache
import requests


class CurrencyConverter(object):
    """Currency rates provider"""

    def __init__(self):
        url = 'http://www.apilayer.net/api/live?' \
              'access_key=f9c1e5189e29b2bdedcc4ac740653e17'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Unexpected response {}'.format(response))

        self.table = response.json()['quotes']

    def get_rate_from_usd(self, to_cur):
        """Returns rate from USD for to_cur currency"""
        target_cur = to_cur.strip().upper()
        if target_cur == 'USD':
            return 1

        rates = [rate for cur, rate in self.table.items()
                 if cur[3:] == target_cur]
        if not rates:
            raise RuntimeError('Unknown currency {}'.format(target_cur))

        return rates[0]

    @lru_cache(maxsize=32)
    def get_rate(self, from_cur, to_cur):
        """Returns currency rate

        :param from_cur: initial currency abbreviation
        :param to_cur:  target currency abbreviation
        """
        initial_rate = self.get_rate_from_usd(from_cur)
        target_rate = self.get_rate_from_usd(to_cur)

        return target_rate / initial_rate


class Money(object):
    """Money class with currency converting functionality"""
    converter = CurrencyConverter()
    operation_currency = 'EUR'
    default_currency = 'USD'

    def __init__(self, amount, currency=None):
        self.amount = amount
        self.currency = currency or self.default_currency

    def __str__(self):
        return '{} {}'.format(self.amount, self.currency)

    def __add__(self, money):
        return Money(
            self.converter.get_rate(
                self.currency,
                self.operation_currency) * self.amount + self.converter.
            get_rate(money.currency,
                     self.operation_currency) * money.amount,
            self.operation_currency)

    def __sub__(self, money):
        return Money(
            self.converter.get_rate(
                self.currency,
                self.operation_currency) * self.amount - self.converter.
            get_rate(money.currency,
                     self.operation_currency) * money.amount,
            self.operation_currency)

    def __neg__(self):
        return Money(- self.converter.get_rate(
            self.currency, self.operation_currency) * self.amount,
            self.operation_currency)

    def __mul__(self, money):
        return Money(money * self.converter.get_rate(
            self.currency, self.operation_currency) * self.amount,
            self.operation_currency)

    __rmul__ = __mul__


if __name__ == '__main__':
    x = Money(10, 'BYN')
    y = Money(11)  # define your own default value, e.g. “USD”
    z = Money(12.34, 'EUR')
    print(z + 3.11 * x + y * 0.8)  # result in “EUR”
