import datetime
import json
from models.account import Account
from models.transaction import Transaction
from utils.helpers import get_accounts, generate_transaction_id, load_json_data
from utils.json_utils import save_to_json
from models.getters.BankGetters import BankGetters 
from data_access_layer.account_repo import save_account  
from data_access_layer.account_repo import save_all_accounts  


def update_account(bank, account_id, new_name):
    bank_getters = BankGetters(bank) 
    bank_id = bank_getters.get_bank_id()  

    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        accounts = all_data.get("accounts", [])
        for account in accounts:
            if account["account_id"] == account_id and account["bank_id"] == bank_id:
                account["account_name"] = new_name
                save_account(account)
                return f"Account {account_id} updated successfully!"
        return "Account not found."
    return "Data file not found."


def delete_account(bank, account_id):
    bank_getters = BankGetters(bank)  
    bank_id = bank_getters.get_bank_id()  

    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        accounts = all_data.get("accounts", [])
        for account in accounts:
            if account["account_id"] == account_id and account["bank_id"] == bank_id:
                accounts.remove(account)

                save_all_accounts(accounts)

                return f"Account {account_id} deleted successfully!"
        return "Account not found."
    return "Data file not found."

