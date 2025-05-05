import datetime
import random

class Account:
    def __init__(self, name, bank_id):
        self._account_id = name[:3].upper() + datetime.datetime.now().strftime("%Y%m%d")
        self._bank_id = bank_id
        self._name = name
        self._password = name.capitalize() + random.choice(["@", "#", "$"]) + str(random.randint(1000, 9999))
        self._balance = 0
        self._transactions = []

    def to_dict(self):
        return {
            "account_id": self._account_id,
            "bank_id": self._bank_id,
            "account_name": self._name,
            "account_password": self._password,
            "account_balance": self._balance
        }
