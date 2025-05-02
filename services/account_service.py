import datetime
from models.account import Account
from models.transaction import Transaction
from utils.helpers import get_accounts, save_bank_data, generate_transaction_id


def deposit(account, amount, currency, exchange_rate):
    if amount <= 0:
        return "Amount must be greater than zero."
    converted_amount = amount * exchange_rate
    account._balance += converted_amount
    txn_id = generate_transaction_id(account._bank_id, account._account_id, "Deposit")
    txn = Transaction(txn_id, account._account_id, "Deposit", converted_amount, currency=currency)
    account._transactions.append(txn)
    return f"Deposited {converted_amount} INR to {account._account_id} successfully!"


def withdraw(account, amount):
    if amount <= 0:
        return "Amount must be greater than zero."
    if account._balance >= amount:
        account._balance -= amount
        txn_id = generate_transaction_id(account._bank_id, account._account_id, "Withdraw")
        txn = Transaction(txn_id, account._account_id, "Withdraw", amount)
        account._transactions.append(txn)
        return f"Withdrawn {amount} INR from {account._account_id} successfully!"
    return "Insufficient balance!"

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
    accounts = get_accounts(bank)
    if account_id in accounts:
        account = accounts[account_id]
        old_name = account._name
        account._name = new_name
        save_bank_data(bank)
        return f"Account {account_id} updated from {old_name} to {new_name} successfully!"
    return "Account not found."

def delete_account(bank, account_id):
    accounts = get_accounts(bank)
    if account_id in accounts:
        del accounts[account_id]
        save_bank_data(bank)
        return f"Account {account_id} deleted successfully!"
    return "Account not found."

def get_account_balance(bank, account_id):
    accounts = get_accounts(bank)
    if account_id in accounts:
        account = accounts[account_id]
        return f"Balance: {account._balance} INR"
    return "Account not found."

def get_transaction_history(account):
    return "\n".join(str(txn) for txn in account._transactions) if account._transactions else "No transactions found."