from services.transaction_service import deposit, withdraw, transfer
from services.account_service import get_account_balance

def deposit_action(bank, account_id):
    amount = float(input("Enter amount: "))
    currency = input("Enter currency (INR by default): ")
    print(deposit(bank, account_id, amount, currency))

def withdraw_action(bank, account_id):
    amount = float(input("Enter amount: "))
    print(withdraw(bank, account_id, amount))

def transfer_action(bank, account_id):
    receiver_id = input("Enter receiver Account ID: ")
    amount = float(input("Enter amount: "))
    same_bank = input("Is the receiver in the same bank? (yes/no): ").lower() == "yes"
    print(transfer(bank, account_id, receiver_id, amount, same_bank))

def check_balance_action(bank, account_id):
    print(get_account_balance(bank, account_id))

def view_transaction_history_action(account_getters):
    transactions = account_getters.get_transactions_string()
    print("\n".join(transactions))