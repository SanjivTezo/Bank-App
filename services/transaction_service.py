from models.transaction import Transaction
from data_access_layer.account_repo import save_account
from data_access_layer.transaction_repo import save_transaction
from models.getters.BankGetters import BankGetters
import datetime
from utils.json_utils import save_to_json
from utils.helpers import load_json_data

def deposit(bank, account_id, amount, currency):
    bank_getters = BankGetters(bank)  

    accounts = bank_getters.get_accounts()  
    account = accounts.get(account_id)
    if not account:
        return "Account not found."

    accepted_currencies = bank_getters.get_accepted_currencies()  
    if currency not in accepted_currencies:
        return f"Currency {currency} not accepted."
    if amount <= 0:
        return "Amount must be greater than zero."

    exchange_rate = accepted_currencies[currency]
    converted_amount = amount * exchange_rate
    account["account_balance"] += converted_amount

    txn_id = f"TXN{bank_getters.get_bank_id()}{account_id}Deposit{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    transaction = Transaction(txn_id, account_id, "Deposit", converted_amount, currency=currency)

    save_transaction(transaction.to_dict())
    save_account(account)

    return f"Deposited {converted_amount} INR to {account_id} successfully!"


def withdraw(bank, account_id, amount):
    bank_getters = BankGetters(bank)  

    accounts = bank_getters.get_accounts()  
    account = accounts.get(account_id)
    if not account:
        return "Account not found."
    if amount <= 0:
        return "Amount must be greater than zero."
    if account["account_balance"] < amount:
        return "Insufficient balance."

    account["account_balance"] -= amount  

    txn_id = f"TXN{bank_getters.get_bank_id()}{account_id}Withdraw{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    transaction = Transaction(txn_id, account_id, "Withdraw", amount)

    save_transaction(transaction.to_dict())
    save_account(account)

    return f"Withdrew {amount} INR from {account_id} successfully!"


def view_all_transactions(bank):
    bank_getters = BankGetters(bank) 
    bank_id = bank_getters.get_bank_id()  
    bank_name = bank_getters.get_bank_name() 

    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        transactions = [
            txn for txn in all_data.get("transactions", [])
            if txn["account_id"] in [acc["account_id"] for acc in all_data.get("accounts", []) if acc["bank_id"] == bank_id]
        ]

        if transactions:
            print(f"Transactions for Bank {bank_name}:")
            for txn in transactions:
                print(f"Transaction ID: {txn['transaction_id']}, Account ID: {txn['account_id']}, "
                      f"Type: {txn['txn_type']}, Amount: {txn['amount']}, "
                      f"Currency: {txn['details'].get('currency', 'N/A')}, Timestamp: {txn['timestamp']}")
        else:
            print(f"No transactions found for Bank {bank_name}.")


def transfer(bank, sender_id, receiver_id, amount, same_bank):
    bank_getters = BankGetters(bank)  

    accounts = bank_getters.get_accounts()  
    sender_account = accounts.get(sender_id)
    if not sender_account:
        return "Sender account not found."

    if same_bank:
       
        receiver_account = accounts.get(receiver_id)
    else:
        
        file_path = "data/bank_data.json"
        all_data = load_json_data(file_path)
        if all_data:
            receiver_account = next(
                (acc for acc in all_data.get("accounts", []) if acc["account_id"] == receiver_id),
                None
            )
        else:
            return "Data file not found."

    if not receiver_account:
        return "Receiver account not found."

    if sender_account["account_balance"] < amount:
        return "Insufficient balance."

    
    sender_account["account_balance"] -= amount
    receiver_account["account_balance"] += amount

   
    sender_txn_id = f"TXN{bank_getters.get_bank_id()}{sender_id}Transfer{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    receiver_txn_id = f"TXN{receiver_account.get('bank_id', bank_getters.get_bank_id())}{receiver_id}Receive{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    
    sender_transaction = Transaction(sender_txn_id, sender_id, "Transfer", -amount, receiver_id=receiver_id)
    receiver_transaction = Transaction(receiver_txn_id, receiver_id, "Receive", amount, sender_id=sender_id)

    save_transaction(sender_transaction.to_dict())
    save_transaction(receiver_transaction.to_dict())
    save_account(sender_account)
    save_account(receiver_account)

    return f"Transferred {amount} successfully. Sender Transaction ID: {sender_txn_id}, Receiver Transaction ID: {receiver_txn_id}"


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