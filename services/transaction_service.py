import datetime
from models.transaction import Transaction
from models.bank import Bank
from utils.json_utils import save_to_json  # Import the utility function
import json
import os
from utils.getters import BankGetters, AccountGetters

def deposit(bank, account_id, amount, currency):
    accounts = bank._accounts  # Access accounts directly from the bank object
    if account_id not in accounts:
        return "Account not found."
    if currency not in bank._accepted_currencies:
        return f"Currency {currency} not accepted."
    if amount <= 0:
        return "Amount must be greater than zero."
    
    # Perform the deposit
    account = accounts[account_id]
    exchange_rate = bank._accepted_currencies[currency]
    converted_amount = amount * exchange_rate
    account._balance += converted_amount
    txn_id = f"TXN{bank._bank_id}{account_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    txn = Transaction(txn_id, account_id, "Deposit", converted_amount, currency=currency)
    account._transactions.append(txn)
    
    # Save updated bank data
    save_to_json("data/bank_data.json", bank._name, bank.to_dict())
    return f"Deposited {converted_amount} INR to {account_id} successfully!"

def withdraw(bank, account_id, amount):
    accounts = bank._accounts  
    if account_id not in accounts:
        return "Account not found."
    if amount <= 0:
        return "Amount must be greater than zero."
    
  
    account = accounts[account_id]
    if account._balance < amount:
        return "Insufficient balance."
    account._balance -= amount
    txn_id = f"TXN{bank._bank_id}{account_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    txn = Transaction(txn_id, account_id, "Withdraw", amount)
    account._transactions.append(txn)
    
   
    save_to_json("data/bank_data.json", bank._name, bank.to_dict())
    return f"Withdrew {amount} INR from {account_id} successfully!"


def view_all_transactions(bank):
    bank_getters = BankGetters(bank)  
    accounts = bank_getters.get_accounts()  
    all_transactions = []

    for account_id, account in accounts.items():
        account_getters = AccountGetters(account) 
        transactions = account_getters.get_transactions_string() 
        all_transactions.extend(transactions)  

    if not all_transactions:
        return "No transactions found."

   
    return "\n".join(all_transactions)
        
def transfer(bank, sender_id, receiver_id, amount, same_bank=True):
    accounts = bank._accounts 
    if sender_id not in accounts:
        return "Sender account not found."
    if amount <= 0:
        return "Amount must be greater than zero."

    if same_bank and receiver_id not in accounts:
        return "Receiver account not found in the same bank."

    other_bank = None
    if not same_bank:
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

    confirm = input(f"Are you sure you want to transfer {amount} INR "
                    f"from {sender_id} to {receiver_id}? (yes/no): ").lower()
    if confirm != "yes":
        return "Transfer cancelled."

    # Calculate charges dynamically based on the transfer type and amount
    if same_bank:
        charges = bank._same_bank_charges.get("RTGS", 0) if amount > 200000 else bank._same_bank_charges.get("IMPS", 0)
    else:
        charges = bank._other_bank_charges.get("RTGS", 0) if amount > 200000 else bank._other_bank_charges.get("IMPS", 0)

    total_debit = amount + (amount * charges / 100)
    sender_account = accounts[sender_id]

    if sender_account._balance < total_debit:
        return "Insufficient balance!"

    # Deduct amount from sender
    sender_account._balance -= total_debit
    txn_id_out = f"TXN{bank._bank_id}{sender_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    txn_sender = Transaction(txn_id_out, sender_id, "Transfer Out", amount, details={"receiver_id": receiver_id, "charges": charges})
    sender_account._transactions.append(txn_sender)

    # Add amount to receiver
    if same_bank:
        receiver_account = accounts[receiver_id]
    else:
        receiver_account = other_bank._accounts[receiver_id]

    receiver_account._balance += amount
    txn_id_in = f"TXN{(bank._bank_id if same_bank else other_bank._bank_id)}{receiver_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    txn_receiver = Transaction(txn_id_in, receiver_id, "Transfer In", amount, details={"sender_id": sender_id})
    receiver_account._transactions.append(txn_receiver)

    # Save updated bank data
    save_to_json("data/bank_data.json", bank._name, bank.to_dict())
    if not same_bank:
        save_to_json("data/bank_data.json", other_bank._name, other_bank.to_dict())

    return (f"{amount} INR transferred from {sender_id} to {receiver_id} "
            f"(charges: {charges}%)")


def revert_transaction(bank, account_id, txn_id):
    bank_getters = BankGetters(bank) 
    accounts = bank_getters.get_accounts()
    if account_id not in accounts:
        return "Account not found."

    account = accounts[account_id]
    account_getters = AccountGetters(account) 

 
    transaction_to_revert = None
    for txn in account_getters.get_transactions():  # Iterate over Transaction objects
        if txn._txn_id == txn_id:
            transaction_to_revert = txn
            break

    if not transaction_to_revert:
        return "Transaction not found."

    txn_type = transaction_to_revert._txn_type
    amount = transaction_to_revert._amount
    details = transaction_to_revert._details

    if txn_type == "Deposit":
        if account._balance < amount:
            return "Insufficient balance to revert deposit."
        account._balance -= amount
        account._transactions.remove(transaction_to_revert)

    elif txn_type == "Withdraw":
        account._balance += amount
        account._transactions.remove(transaction_to_revert)

    elif txn_type == "Transfer Out":
        receiver_id = details["receiver_id"]
        receiver_account = accounts.get(receiver_id)
        if not receiver_account:
            return "Receiver account not found."

        receiver_account._balance -= amount
        account._balance += amount

        # Remove the corresponding "Transfer In" transaction from the receiver
        for txn in receiver_account._transactions:
            if txn._txn_type == "Transfer In" and txn._details.get("sender_id") == account_id and txn._amount == amount:
                receiver_account._transactions.remove(txn)
                break

        account._transactions.remove(transaction_to_revert)

    # Save updated bank data
    save_to_json("data/bank_data.json", bank._name, bank.to_dict())
    return f"Transaction {txn_id} reverted successfully!"