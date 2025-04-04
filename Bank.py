import datetime
import json
import os
from account import Account
from transaction import Transaction

class Bank:
    def __init__(self, name):
        self._name = name  
        self._bank_id = name[:3].upper() + datetime.datetime.now().strftime("%Y%m%d")  
        self._same_bank_charges = {"RTGS": 0, "IMPS": 5}  
        self._other_bank_charges = {"RTGS": 2, "IMPS": 6}  
        self._accepted_currencies = {"INR": 1}  
        self._accounts = {}  
        self.load_from_json()
        print(f"\nWelcome to {self._name} Bank!")

    def to_dict(self):
        return {
            "name": self._name,
            "bank_id": self._bank_id,
            "same_bank_charges": self._same_bank_charges,
            "other_bank_charges": self._other_bank_charges,
            "accepted_currencies": self._accepted_currencies,
            "accounts": {acc_id: acc.to_dict() for acc_id, acc in self._accounts.items()}
        }

    def save_to_json(self):
        with open("data/bank_data.json", "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    def load_from_json(self):
        if os.path.exists("data/bank_data.json"):
            with open("data/bank_data.json", "r") as file:
                data = json.load(file)
                self._same_bank_charges = data.get("same_bank_charges", {"RTGS": 0, "IMPS": 5})
                self._other_bank_charges = data.get("other_bank_charges", {"RTGS": 2, "IMPS": 6})
                self._accepted_currencies = data.get("accepted_currencies", {"INR": 1})
                self._accounts = {}
                for acc_id, acc_data in data.get("accounts", {}).items():
                    account = Account(acc_data["name"], acc_data["bank_id"])
                    account._account_id = acc_data["account_id"]
                    account._password = acc_data["password"]
                    account._balance = acc_data["balance"]
                    account._transactions = [Transaction(txn["txn_id"], txn["account_id"], txn["txn_type"], txn["amount"], **txn["details"]) for txn in acc_data["transactions"]]
                    self._accounts[acc_id] = account

    def get_bank_id(self):
        return self._bank_id

    def get_accepted_currencies(self):
        return self._accepted_currencies

    def get_accounts(self):
        return self._accounts