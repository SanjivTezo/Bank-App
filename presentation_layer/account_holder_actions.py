from services.transaction_service import withdraw, transfer, deposit
from utils.helpers import load_json_data

def deposit_action(bank, account_id):
    amount = float(input("Enter amount to deposit: "))
    currency = input("Enter currency (e.g., INR, USD): ")
    result = deposit(bank, account_id, amount, currency)
    print(result)

def withdraw_action(bank, account_id):
    amount = float(input("Enter amount to withdraw: "))
    result = withdraw(bank, account_id, amount)
    print(result)

def transfer_action(bank, account_id):
    receiver_id = input("Enter receiver Account ID: ")
    amount = float(input("Enter amount to transfer: "))
    same_bank = input("Is the receiver in the same bank? (yes/no): ").lower() == "yes"
    result = transfer(bank, account_id, receiver_id, amount, same_bank)
    print(result)

def check_balance_action(bank, account_id):
    account = bank._accounts.get(account_id)
    if account:
        print(f"Account Balance: {account['account_balance']}")
    else:
        print("Account not found.")

def view_transaction_history_action(bank, account_id):
    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        transactions = [
            txn for txn in all_data.get("transactions", [])
            if txn["account_id"] == account_id
        ]

        if transactions:
            print(f"Transaction History for Account {account_id}:")
            for txn in transactions:
                print(f"Transaction ID: {txn['transaction_id']}, Type: {txn['txn_type']}, "
                      f"Amount: {txn['amount']}, Currency: {txn['details'].get('currency', 'N/A')}, "
                      f"Timestamp: {txn['timestamp']}")
        else:
            print("No transactions found for this account.")