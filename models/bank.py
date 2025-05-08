import datetime
import os
from utils.json_utils import  load_from_json

class Bank:
    def __init__(self, name, admin_user, admin_pass):
        self._admin_user = admin_user
        self._admin_pass = admin_pass
        self._name = name
        self._bank_id = name[:3].upper() + datetime.datetime.now().strftime("%Y%m%d")
        self._same_bank_charges = {"RTGS": 0, "IMPS": 5}
        self._other_bank_charges = {"RTGS": 2, "IMPS": 6}
        self._accepted_currencies = {"INR": 1}
        self._accounts = {}

        os.makedirs("data", exist_ok=True)
        load_from_json(self)

    def to_dict(self):
        return {
            "bank_id": self._bank_id,
            "bank_name": self._name,
            "admin_user": self._admin_user,
            "admin_pass": self._admin_pass
        }

    def to_charges_dict(self):
        return {
            "bank_id": self._bank_id,
            "bank_name": self._name,
            "same_bank_charges": self._same_bank_charges,
            "other_bank_charges": self._other_bank_charges
        }

    def to_accepted_currencies_dict(self):
        return {
            "bank_id": self._bank_id,
            "bank_name": self._name,
            "accepted_currencies": self._accepted_currencies
        }