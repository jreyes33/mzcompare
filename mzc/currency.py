class Currency(object):
    """Class for performing currency transformations."""

    def __init__(self, name):
        self.name = name
        self.rates = {"USD": 7.4234, "EUR": 9.1775, "SEK": 1,
                      "MM": 1, "UYU": 0.256963, "R$": 2.62589,
                      "GBP": 13.35247, "DKK": 1.23522, "NOK": 1.07245,
                      "CHF": 5.86737, "CAD": 5.70899, "AUD": 5.66999,
                      "ILS": 1.6953, "MXN": 0.68576, "ARS": 2.64445,
                      "BOB": 0.939, "PYG": 0.001309, "RUB": 0.26313,
                      "PLN": 1.95278, "ISK": 0.10433, "BGL": 4.70738,
                      "ZAR": 1.23733, "US$": 7.4234, "THB": 0.17079,
                      "SIT": 0.03896, "SKK": 0.24946, "JPY": 0.06,
                      "INR": 0.17, "MZ": 1}

    def convert_from(self, currency_name, value):
        if self.name in self.rates and currency_name in self.rates:
            return int(round(int(value) * self.rates[currency_name] /
                             self.rates[self.name]))
        else:
            return -1

    def convert_to(self, currency_name, value):
        if self.name in self.rates and currency_name in self.rates:
            return int(round(int(value) * self.rates[self.name] /
                             self.rates[currency_name]))
        else:
            return -1
