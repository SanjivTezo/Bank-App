import json
import os
import datetime
from models.bank import Bank
from utils.getters import BankGetters
from utils.json_utils import save_to_json

def load_json_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        print("Data file not found.")
        return None

def load_bank(file_path, bank_name):
    all_data = load_json_data(file_path)  

    if all_data:
        bank_data = next((bank for bank in all_data.get("bank", []) if bank["bank_name"] == bank_name), None)
        if not bank_data:
            return None, "Bank Does Not Exist"

        bank = Bank(bank_data["bank_name"], bank_data["admin_user"], bank_data["admin_pass"])

        accepted_currencies = next(
            (entry["accepted_currencies"] for entry in all_data.get("accepted_currencies", [])
             if entry["bank_id"] == bank._bank_id),
            {}
        )
        bank._accepted_currencies = accepted_currencies

        accounts = all_data.get("accounts", [])
        bank._accounts = {acc["account_id"]: acc for acc in accounts if acc["bank_id"] == bank._bank_id}

        return bank, None

    return None, "No banks available. Please create a bank first."

def get_accounts(bank):
    bank_getters = BankGetters(bank)
    return bank_getters.get_accounts()

def save_bank_data(bank):
    save_to_json("data/bank_data.json", bank._name, bank.to_dict())

def generate_transaction_id(bank_id, account_id, txn_type):
    return f"TXN{bank_id}{account_id}{txn_type}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

def validate_account(accounts, account_id):
    if account_id not in accounts:
        return None, "Account not found."
    return accounts[account_id], None