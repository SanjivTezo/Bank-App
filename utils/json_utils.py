import os
import json
from models.account import Account
from models.transaction import Transaction
from utils.getters import AccountGetters, BankGetters, TransactionGetters


def save_to_json(file_path, section, data):
    try:
        existing_data = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                existing_data = json.load(file)

        if section not in existing_data:
            existing_data[section] = []

        if isinstance(data, list):
            existing_data[section] = data
        else:
            section_data = existing_data[section]
            if section == "transactions":
                for item in section_data:
                    if item.get("transaction_id") == data.get("transaction_id"):
                        item.update(data)
                        break
                else:
                    section_data.append(data)
            elif section == "accounts":
                for item in section_data:
                    if item.get("account_id") == data.get("account_id"):
                        item.update(data)
                        break
                else:
                    section_data.append(data)
            else:
                for item in section_data:
                    if item.get("bank_id") == data.get("bank_id"):
                        item.update(data)
                        break
                else:
                    section_data.append(data)

        with open(file_path, "w") as file:
            json.dump(existing_data, file, indent=4)

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving data to JSON: {str(e)}")

        
def load_from_json(self):
    try:
        if os.path.exists("data/bank_data.json"):
            with open("data/bank_data.json", "r") as file:
                all_banks = json.load(file)

                if self._name in all_banks:
                    data = all_banks[self._name]

                    self._bank_id = data.get("bank_id", self._bank_id)  
                    self._admin_user = data.get("admin_user", self._admin_user)
                    self._admin_pass = data.get("admin_pass", self._admin_pass)
                    self._same_bank_charges = data.get("same_bank_charges", {"RTGS": 0, "IMPS": 5})
                    self._other_bank_charges = data.get("other_bank_charges", {"RTGS": 2, "IMPS": 6})
                    self._accepted_currencies = data.get("accepted_currencies", {"INR": 1})
                    self._accounts = {}

                    
                    for acc_id, acc_data in data.get("accounts", {}).items():
                        account = Account(acc_data["name"], self._bank_id)  
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

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading bank data: {str(e)}")

