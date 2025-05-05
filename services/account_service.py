import datetime
import json
import os
from models.account import Account
from models.transaction import Transaction
from utils.helpers import get_accounts, save_bank_data, generate_transaction_id
from utils.json_utils import save_to_json


def deposit(account, amount, currency, exchange_rate):
    if amount <= 0:
        return "Amount must be greater than zero."
    converted_amount = amount * exchange_rate
    account._balance += converted_amount
    txn_id = generate_transaction_id(account._bank_id, account._account_id, "Deposit")
    txn = Transaction(txn_id, account._account_id, "Deposit", converted_amount, currency=currency)
    account._transactions.append(txn)
    return f"Deposited {converted_amount} INR to {account._account_id} successfully!"


def withdraw(bank, account_id, amount):
    account = bank._accounts.get(account_id)
    if not account:
        return "Account not found."

    if account["account_balance"] < amount:
        return "Insufficient balance."
   
    account["account_balance"] -= amount

    save_to_json("data/bank_data.json", "accounts", account)


    txn_id = f"TXN{bank._bank_id}{account_id}Withdraw{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    transaction = Transaction(txn_id, account_id, "Withdraw", amount)
    save_to_json("data/bank_data.json", "transactions", transaction.to_dict())

    return f"Withdrawn {amount} successfully. Transaction ID: {txn_id}"


def create_account(bank, name):
    accounts = get_accounts(bank)
    while True:
        account_id = f"{name[:3].upper()}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        if account_id not in accounts:
            break

    account = Account(name, bank._bank_id)
    account._account_id = account_id
    accounts[account_id] = account
    save_bank_data(bank)
    return f"Account created! ID: {account_id}, Password: {account._password}"


def update_account(bank, account_id, new_name):

    file_path = "data/bank_data.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            all_data = json.load(file)

        accounts = all_data.get("accounts", [])
        for account in accounts:
            if account["account_id"] == account_id and account["bank_id"] == bank._bank_id:
                account["account_name"] = new_name

                with open(file_path, "w") as file:
                    json.dump(all_data, file, indent=4)

                return f"Account {account_id} updated successfully!"
        return "Account not found."
    return "Data file not found."


def delete_account(bank, account_id):
    file_path = "data/bank_data.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            all_data = json.load(file)

        accounts = all_data.get("accounts", [])
        for account in accounts:
            if account["account_id"] == account_id and account["bank_id"] == bank._bank_id:
                accounts.remove(account)

                with open(file_path, "w") as file:
                    json.dump(all_data, file, indent=4)

                return f"Account {account_id} deleted successfully!"
        return "Account not found."
    return "Data file not found."


def get_account_balance(bank, account_id):
    accounts = get_accounts(bank)
    if account_id in accounts:
        account = accounts[account_id]
        return f"Balance: {account._balance} INR"
    return "Account not found."


def get_transaction_history(account):
    return "\n".join(str(txn) for txn in account._transactions) if account._transactions else "No transactions found."