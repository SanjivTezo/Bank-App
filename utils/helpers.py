import json
import os
import datetime
from models.bank import Bank
from utils.getters import BankGetters
from utils.json_utils import save_to_json

def load_bank(file_path, bank_name):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            all_banks = json.load(file)
        if bank_name not in all_banks:
            return None, "Bank Does Not Exist"
        bank_data = all_banks[bank_name]
        bank = Bank(bank_data["name"], bank_data["admin_user"], bank_data["admin_pass"])
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