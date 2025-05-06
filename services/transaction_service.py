from models.transaction import Transaction
from models.bank import Bank
from utils.helpers import save_bank_data, generate_transaction_id, validate_account, save_to_json, load_json_data
import datetime

def deposit(bank, account_id, amount, currency):
    account = bank._accounts.get(account_id)
    if not account:
        return "Account not found."
    if currency not in bank._accepted_currencies:
        return f"Currency {currency} not accepted."
    if amount <= 0:
        return "Amount must be greater than zero."

    exchange_rate = bank._accepted_currencies[currency]
    converted_amount = amount * exchange_rate
    account["account_balance"] += converted_amount

    txn_id = f"TXN{bank._bank_id}{account_id}Deposit{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    transaction = Transaction(txn_id, account_id, "Deposit", converted_amount, currency=currency)
    save_to_json("data/bank_data.json", "transactions", transaction.to_dict())
    save_to_json("data/bank_data.json", "accounts", account)

    return f"Deposited {converted_amount} INR to {account_id} successfully!"


def withdraw(bank, account_id, amount):
    account = bank._accounts.get(account_id)
    if not account:
        return "Account not found."
    if amount <= 0:
        return "Amount must be greater than zero."
    if account["account_balance"] < amount:
        return "Insufficient balance."

    account["account_balance"] -= amount

    txn_id = f"TXN{bank._bank_id}{account_id}Withdraw{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    transaction = Transaction(txn_id, account_id, "Withdraw", amount)
    save_to_json("data/bank_data.json", "transactions", transaction.to_dict())
    save_to_json("data/bank_data.json", "accounts", account)

    return f"Withdrew {amount} INR from {account_id} successfully!"

def view_all_transactions(bank):
    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        transactions = [
            txn for txn in all_data.get("transactions", [])
            if txn["account_id"] in [acc["account_id"] for acc in all_data.get("accounts", []) if acc["bank_id"] == bank._bank_id]
        ]

        if transactions:
            print(f"Transactions for Bank {bank._name}:")
            for txn in transactions:
                print(f"Transaction ID: {txn['transaction_id']}, Account ID: {txn['account_id']}, "
                      f"Type: {txn['txn_type']}, Amount: {txn['amount']}, "
                      f"Currency: {txn['details'].get('currency', 'N/A')}, Timestamp: {txn['timestamp']}")
        else:
            print(f"No transactions found for Bank {bank._name}.")

def transfer(bank, sender_id, receiver_id, amount, same_bank):
    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        sender_account = bank._accounts.get(sender_id)
        if not sender_account:
            return "Sender account not found."

        if same_bank:
            receiver_account = bank._accounts.get(receiver_id)
        else:
            receiver_account = next(
                (acc for acc in all_data.get("accounts", []) if acc["account_id"] == receiver_id),
                None
            )

        if not receiver_account:
            return "Receiver account not found."

        if sender_account["account_balance"] < amount:
            return "Insufficient balance."

        sender_account["account_balance"] -= amount
        save_to_json(file_path, "accounts", sender_account)

        receiver_account["account_balance"] += amount
        save_to_json(file_path, "accounts", receiver_account)

        sender_txn_id = f"TXN{bank._bank_id}{sender_id}Transfer{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        sender_transaction = Transaction(sender_txn_id, sender_id, "Transfer", -amount, receiver_id=receiver_id)
        save_to_json(file_path, "transactions", sender_transaction.to_dict())

        receiver_txn_id = f"TXN{receiver_account['bank_id']}{receiver_id}Receive{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        receiver_transaction = Transaction(receiver_txn_id, receiver_id, "Receive", amount, sender_id=sender_id)
        save_to_json(file_path, "transactions", receiver_transaction.to_dict())

        return f"Transferred {amount} successfully. Sender Transaction ID: {sender_txn_id}, Receiver Transaction ID: {receiver_txn_id}"
    return "Data file not found."

def revert_transaction(bank, account_id, txn_id):
    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        transactions = all_data.get("transactions", [])
        transaction_to_revert = next((txn for txn in transactions if txn["transaction_id"] == txn_id), None)
        if not transaction_to_revert:
            return "Transaction not found."

        accounts = all_data.get("accounts", [])
        account = next((acc for acc in accounts if acc["account_id"] == account_id), None)
        if not account:
            return "Account not found."

        txn_type = transaction_to_revert["txn_type"]
        amount = transaction_to_revert["amount"]

        if txn_type == "Deposit":
            if account["account_balance"] < amount:
                return "Insufficient balance to revert deposit."
            account["account_balance"] -= amount
        elif txn_type == "Withdraw":
            account["account_balance"] += amount
        elif txn_type == "Transfer":
            receiver_id = transaction_to_revert["details"]["receiver_id"]
            receiver_account = next((acc for acc in accounts if acc["account_id"] == receiver_id), None)
            if not receiver_account:
                return "Receiver account not found."
            account["account_balance"] += abs(amount)
            receiver_account["account_balance"] -= abs(amount)
        elif txn_type == "Receive":
            sender_id = transaction_to_revert["details"]["sender_id"]
            sender_account = next((acc for acc in accounts if acc["account_id"] == sender_id), None)
            if not sender_account:
                return "Sender account not found."
            account["account_balance"] -= abs(amount)
            sender_account["account_balance"] += abs(amount)
        else:
            return f"Cannot revert transaction of type {txn_type}."

        transactions.remove(transaction_to_revert)

        save_to_json(file_path, "transactions", transactions)
        save_to_json(file_path, "accounts", accounts)

        return f"Transaction {txn_id} reverted successfully!"
    return "Data file not found."