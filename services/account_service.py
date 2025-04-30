import datetime
from models.account import Account
from models.bank import Bank
from models.transaction import Transaction
from utils.getters import AccountGetters, BankGetters, TransactionGetters
from utils.json_utils import save_to_json, load_from_json

def deposit(self, amount, currency, exchange_rate):
        if amount <= 0:
            return "Amount must be greater than zero."
        converted_amount = amount * exchange_rate
        self._balance += converted_amount
        txn_id = f"TXN{self._bank_id}{self._account_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        txn = Transaction(txn_id, self._account_id, "Deposit", converted_amount, currency=currency)
        self._transactions.append(txn)
        return f"Deposited {converted_amount} INR to {self._account_id} successfully!"

def withdraw(self, amount):
        if amount <= 0:
            return "Amount must be greater than zero."
        if self._balance >= amount:
            self._balance -= amount
            txn_id = f"TXN{self._bank_id}{self._account_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            txn = Transaction(txn_id, self._account_id, "Withdraw", amount)
            self._transactions.append(txn)
            return f"Withdrawn {amount} INR from {self._account_id} successfully!"
        return "Insufficient balance!"

def get_transaction_history(self):
        return "\n".join(str(txn) for txn in self._transactions) if self._transactions else "No transactions found."

def __str__(self):
        return f"Account[ID: {self._account_id}, Name: {self._name}, Balance: {self._balance}]"
 


def create_account(bank, name):
    bank_getters = BankGetters(bank)  
    accounts = bank_getters.get_accounts()  
  
    while True:
        account_id = f"{name[:3].upper()}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        if account_id not in accounts:
            break

  
    account = Account(name, bank._bank_id)
    account._account_id = account_id
    accounts[account_id] = account 

   
    save_to_json("data/bank_data.json", bank._name, bank.to_dict())
    return f"Account created! ID: {account_id}, Password: {account._password}"



def update_account(bank, account_id, new_name):
    bank_getters = BankGetters(bank)  
    accounts = bank_getters.get_accounts() 
    if account_id in accounts:
        account = accounts[account_id]
        account_getters = AccountGetters(account) 
        old_name = account_getters.get_name() 
        account._name = new_name 
        save_to_json("data/bank_data.json", bank._name, bank.to_dict())  
        return f"Account {account_id} updated from {old_name} to {new_name} successfully!"
    return "Account not found."


def delete_account(bank, account_id):
    bank_getters = BankGetters(bank)  
    accounts = bank_getters.get_accounts()  
    if account_id in accounts:
        del accounts[account_id] 
        save_to_json("data/bank_data.json", bank._name, bank.to_dict())  
        return f"Account {account_id} deleted successfully!"
    return "Account not found."

def get_account_balance(bank, account_id):
    bank_getters = BankGetters(bank) 
    accounts = bank_getters.get_accounts()  
    if account_id in accounts:
        account = accounts[account_id]
        account_getters = AccountGetters(account)  
        return f"Balance: {account_getters.get_balance()} INR" 
    return "Account not found."