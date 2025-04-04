import datetime
import random
from transaction import Transaction

class Account:
    def __init__(self, name, bank_id):
        self._account_id = name[:3].upper() + datetime.datetime.now().strftime("%Y%m%d")  
        self._bank_id = bank_id  
        self._name = name 
        self._password = name.capitalize() + random.choice(["@", "#", "$"]) + str(random.randint(1000, 9999))
        self._balance = 0  
        self._transactions = []  

    def to_dict(self):
        return {
            "account_id": self._account_id,
            "bank_id": self._bank_id,
            "name": self._name,
            "password": self._password,
            "balance": self._balance,
            "transactions": [txn.to_dict() for txn in self._transactions]
        }

    # Getter methods 
    def get_account_id(self):
        return self._account_id

    def get_name(self):
        return self._name

    def get_balance(self):
        return self._balance

    def get_transactions(self):
        return self._transactions

    def verify_password(self, password):
        return self._password == password

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