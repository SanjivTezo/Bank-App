from models.transaction import Transaction
from models.bank import Bank
from utils.helpers import save_bank_data, generate_transaction_id, validate_account
import json
import os

def deposit(bank, account_id, amount, currency):
    accounts = bank._accounts
    account, error = validate_account(accounts, account_id)
    if error:
        return error
    if currency not in bank._accepted_currencies:
        return f"Currency {currency} not accepted."
    if amount <= 0:
        return "Amount must be greater than zero."

    exchange_rate = bank._accepted_currencies[currency]
    converted_amount = amount * exchange_rate
    account._balance += converted_amount
    txn_id = generate_transaction_id(bank._bank_id, account_id, "Deposit")
    txn = Transaction(txn_id, account_id, "Deposit", converted_amount, currency=currency)
    account._transactions.append(txn)

    save_bank_data(bank)
    return f"Deposited {converted_amount} INR to {account_id} successfully!"

def withdraw(bank, account_id, amount):
    accounts = bank._accounts
    account, error = validate_account(accounts, account_id)
    if error:
        return error
    if amount <= 0:
        return "Amount must be greater than zero."
    if account._balance < amount:
        return "Insufficient balance."

    account._balance -= amount
    txn_id = generate_transaction_id(bank._bank_id, account_id, "Withdraw")
    txn = Transaction(txn_id, account_id, "Withdraw", amount)
    account._transactions.append(txn)

    save_bank_data(bank)
    return f"Withdrew {amount} INR from {account_id} successfully!"

def view_all_transactions(bank):
    accounts = bank._accounts
    all_transactions = []

    for account_id, account in accounts.items():
        transactions = [str(txn) for txn in account._transactions]
        all_transactions.extend(transactions)

    if not all_transactions:
        return "No transactions found."
    return "\n".join(all_transactions)

def transfer(bank, sender_id, receiver_id, amount, same_bank=True):
    accounts = bank._accounts
    sender_account, error = validate_account(accounts, sender_id)
    if error:
        return error
    if amount <= 0:
        return "Amount must be greater than zero."

    if same_bank:
        receiver_account, error = validate_account(accounts, receiver_id)
        if error:
            return error
    else:
        other_bank_name = input("Enter receiver's Bank Name: ")
        filepath = "data/bank_data.json"
        if not os.path.exists(filepath):
            return "No banks data available."
        with open(filepath, "r") as f:
            all_banks = json.load(f)
        if other_bank_name not in all_banks:
            return f"Bank '{other_bank_name}' not found."
        ob = all_banks[other_bank_name]
        other_bank = Bank(ob["name"], ob["admin_user"], ob["admin_pass"])
        if receiver_id not in other_bank._accounts:
            return "Receiver account not found in that bank."
        receiver_account = other_bank._accounts[receiver_id]

    charges = (bank._same_bank_charges if same_bank else bank._other_bank_charges)
    charge_type = "RTGS" if amount > 200000 else "IMPS"
    charge_percentage = charges.get(charge_type, 0)
    total_debit = amount + (amount * charge_percentage / 100)

    if sender_account._balance < total_debit:
        return "Insufficient balance!"

    sender_account._balance -= total_debit
    txn_id_out = generate_transaction_id(bank._bank_id, sender_id, "Transfer Out")
    txn_sender = Transaction(txn_id_out, sender_id, "Transfer Out", amount, details={"receiver_id": receiver_id, "charges": charge_percentage})
    sender_account._transactions.append(txn_sender)

    receiver_account._balance += amount
    txn_id_in = generate_transaction_id(bank._bank_id if same_bank else other_bank._bank_id, receiver_id, "Transfer In")
    txn_receiver = Transaction(txn_id_in, receiver_id, "Transfer In", amount, details={"sender_id": sender_id})
    receiver_account._transactions.append(txn_receiver)

    save_bank_data(bank)
    if not same_bank:
        save_bank_data(other_bank)

    return f"{amount} INR transferred from {sender_id} to {receiver_id} (charges: {charge_percentage}%)"

def revert_transaction(bank, account_id, txn_id):
    accounts = bank._accounts
    account, error = validate_account(accounts, account_id)
    if error:
        return error

    transaction_to_revert = next((txn for txn in account._transactions if txn._txn_id == txn_id), None)
    if not transaction_to_revert:
        return "Transaction not found."

    txn_type = transaction_to_revert._txn_type
    amount = transaction_to_revert._amount
    details = transaction_to_revert._details

    if txn_type == "Deposit":
        if account._balance < amount:
            return "Insufficient balance to revert deposit."
        account._balance -= amount
    elif txn_type == "Withdraw":
        account._balance += amount
    elif txn_type == "Transfer Out":
        receiver_id = details["receiver_id"]
        receiver_account, error = validate_account(accounts, receiver_id)
        if error:
            return error
        receiver_account._balance -= amount
        account._balance += amount
        receiver_account._transactions = [txn for txn in receiver_account._transactions if not (txn._txn_type == "Transfer In" and txn._details.get("sender_id") == account_id and txn._amount == amount)]

    account._transactions.remove(transaction_to_revert)
    save_bank_data(bank)
    return f"Transaction {txn_id} reverted successfully!"