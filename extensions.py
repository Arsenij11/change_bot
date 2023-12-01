from config import keys
import telebot
import requests
import json

API_KEY = "API_KEY"

class countofvalues(Exception):
    pass

class equalvalues(Exception):
    pass

class keyisnotexist(Exception):
    pass

class currencychecking:
    @staticmethod
    def convert(message: telebot.types.Message):
        try:
            values = message.text.split(' ')
            if len(values) != 3:
                raise countofvalues
            base, quote, amount = values
            if quote == base:
                raise equalvalues
            if checking.find_key_by_value(keys, quote) is None or checking.find_key_by_value(keys, base) is None:
                raise keyisnotexist
            amount = float(amount)
        except keyisnotexist as error:
            if checking.find_key_by_value(keys, quote) is None:
                return quote,error
            elif checking.find_key_by_value(keys, base) is None:
                return base, error
        except countofvalues as error:
            return values, error
        except equalvalues as error:
            return values, error
        except ValueError as error:
            return values, error
        else:
            error = None
            return values, error
class API:
    @staticmethod
    def get_price(values):
        try:
            base, quote, amount = values
            r = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base}/{quote}/{amount}")
        except Exception as e:
            return e
        else:
            total_base = json.loads(r.content)['conversion_result']
            text = f'Цена {amount} {checking.find_key_by_value(keys, base)} в {checking.find_key_by_value(keys, quote)} - {total_base}'
            return text

class checking:
    @staticmethod
    def find_key_by_value(dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None