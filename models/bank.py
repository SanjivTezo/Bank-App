import datetime
import json
import os
from models.account import Account  
from models.transaction import Transaction

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
        
        self.load_from_json()
        # print(f"\nWelcome to {self._name} Bank!")

    def to_dict(self):
        return {
            "name": self._name,
            "admin_user": self._admin_user,
            "admin_pass": self._admin_pass,
            "bank_id": self._bank_id,
            "same_bank_charges": self._same_bank_charges,
            "other_bank_charges": self._other_bank_charges,
            "accepted_currencies": self._accepted_currencies,
            "accounts": {acc_id: acc.to_dict() for acc_id, acc in self._accounts.items()}
        }
    
    def save_to_json(self):
        try:
            data = {}
            if os.path.exists("data/bank_data.json"):
                with open("data/bank_data.json", "r") as file:
                    data = json.load(file)
            # Save or update this bank's data
            data[self._name] = self.to_dict()

            with open("data/bank_data.json", "w") as file:
                json.dump(data, file, indent=4)

        except (IOError, json.JSONEncodeError) as e:
            print(f"Error saving bank data: {str(e)}")

    def load_from_json(self):
            try:
                if os.path.exists("data/bank_data.json"):
                    with open("data/bank_data.json", "r") as file:
                        all_banks = json.load(file)

                        if self._name in all_banks:
                            data = all_banks[self._name]

                            self._same_bank_charges = data.get("same_bank_charges", {"RTGS": 0, "IMPS": 5})
                            self._other_bank_charges = data.get("other_bank_charges", {"RTGS": 2, "IMPS": 6})
                            self._accepted_currencies = data.get("accepted_currencies", {"INR": 1})
                            self._accounts = {}

                            for acc_id, acc_data in data.get("accounts", {}).items():
                                try:
                                    account = Account(acc_data["name"], acc_data["bank_id"])
                                    account._account_id = acc_data["account_id"]
                                    account._password = acc_data["password"]
                                    account._balance = acc_data["balance"]
                                    account._transactions = [
                                        Transaction(
                                            txn["txn_id"],
                                            txn["account_id"],
                                            txn["txn_type"],
                                            txn["amount"],
                                            **txn.get("details", {})
                                        ) for txn in acc_data.get("transactions", [])
                                    ]
                                    self._accounts[acc_id] = account
                                except KeyError as e:
                                    print(f"Error loading account {acc_id}: {str(e)}")

            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading bank data: {str(e)}")

    def get_bank_id(self):
        return self._bank_id

    def get_accepted_currencies(self):
        return self._accepted_currencies

    def get_accounts(self):
        return self._accounts
    def get_username(self):
        return self._admin_user
    def get_password(self):
        return self._admin_pass