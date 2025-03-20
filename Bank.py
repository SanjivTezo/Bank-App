import datetime
import random
import json
import os

class Transaction:
    def __init__(self, txn_id, account_id, txn_type, amount, **kwargs):
        self._txn_id = txn_id  
        self._account_id = account_id  
        self._txn_type = txn_type  
        self._amount = amount  
        self._details = kwargs  
        self._timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    def __str__(self):
        return f"Transaction[ID: {self._txn_id}, Type: {self._txn_type}, Amount: {self._amount}, Details: {self._details}, Timestamp: {self._timestamp}]"

    def to_dict(self):
        return {
            "txn_id": self._txn_id,
            "account_id": self._account_id,
            "txn_type": self._txn_type,
            "amount": self._amount,
            "details": self._details,
            "timestamp": self._timestamp
        }

    def get_txn_id(self):
        return self._txn_id

    def get_account_id(self):
        return self._account_id

    def get_txn_type(self):
        return self._txn_type

    def get_amount(self):
        return self._amount

    def get_details(self):
        return self._details

    def get_timestamp(self):
        return self._timestamp


class Account:
    def __init__(self, name, bank_id):
        self._account_id = name[:3].upper() + datetime.datetime.now().strftime("%Y%m%d")  
        self._bank_id = bank_id  
        self._name = name 
        # self._password = str(random.randint(1000, 9999))  
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


class Bank:
    def __init__(self, name):
        self._name = name  
        self._bank_id = name[:3].upper() + datetime.datetime.now().strftime("%Y%m%d")  
        self._same_bank_charges = {"RTGS": 0, "IMPS": 5}  
        self._other_bank_charges = {"RTGS": 2, "IMPS": 6}  
        self._accepted_currencies = {"INR": 1}  
        self._accounts = {}  
        self.load_from_json()
        print(f"\nWelcome to {self._name} Bank!")

    def to_dict(self):
        return {
            "name": self._name,
            "bank_id": self._bank_id,
            "same_bank_charges": self._same_bank_charges,
            "other_bank_charges": self._other_bank_charges,
            "accepted_currencies": self._accepted_currencies,
            "accounts": {acc_id: acc.to_dict() for acc_id, acc in self._accounts.items()}
        }

    def save_to_json(self):
        with open("bank_data.json", "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    def load_from_json(self):
        if os.path.exists("bank_data.json"):
            with open("bank_data.json", "r") as file:
                data = json.load(file)
                self._same_bank_charges = data.get("same_bank_charges", {"RTGS": 0, "IMPS": 5})
                self._other_bank_charges = data.get("other_bank_charges", {"RTGS": 2, "IMPS": 6})
                self._accepted_currencies = data.get("accepted_currencies", {"INR": 1})
                self._accounts = {}
                for acc_id, acc_data in data.get("accounts", {}).items():
                    account = Account(acc_data["name"], acc_data["bank_id"])
                    account._account_id = acc_data["account_id"]
                    account._password = acc_data["password"]
                    account._balance = acc_data["balance"]
                    account._transactions = [Transaction(txn["txn_id"], txn["account_id"], txn["txn_type"], txn["amount"], **txn["details"]) for txn in acc_data["transactions"]]
                    self._accounts[acc_id] = account

    def get_bank_id(self):
        return self._bank_id

    def get_accepted_currencies(self):
        return self._accepted_currencies

    def get_accounts(self):
        return self._accounts

    def create_account(self, name):
        account = Account(name, self._bank_id)
        self._accounts[account.get_account_id()] = account
        self.save_to_json()
        return f"Account created! ID: {account.get_account_id()}, Password: {account._password}"

    def update_account(self, account_id, new_name):
        if account_id in self._accounts:
            old_name = self._accounts[account_id].get_name()
            self._accounts[account_id]._name = new_name
            self.save_to_json()
            return f"Account {account_id} updated from {old_name} to {new_name} successfully!"
        return "Account not found."

    def delete_account(self, account_id):
        if account_id in self._accounts:
            del self._accounts[account_id]
            self.save_to_json()
            return "Account deleted successfully!"
        return "Account not found."

    def add_currency(self, currency, exchange_rate):
        self._accepted_currencies[currency] = exchange_rate
        self.save_to_json()
        return f"{currency} added with exchange rate {exchange_rate}"

    def display_currency_details(self):
        if not self._accepted_currencies:
            print("\nNo currencies available.")
            return
        print("\nAll Currency Details:")
        for currency, exchange_rate in self._accepted_currencies.items():
            print(f"{currency}: {exchange_rate}")

    # Polymorphism
    def set_charges(self, rtgs_charge, imps_charge, same_bank=True):
        if same_bank:
            self._same_bank_charges = {"RTGS": rtgs_charge, "IMPS": imps_charge}
            self.save_to_json()
            return f"Same Bank Charges set to RTGS: {rtgs_charge}%, IMPS: {imps_charge}%"
        else:
            self._other_bank_charges = {"RTGS": rtgs_charge, "IMPS": imps_charge}
            self.save_to_json()
            return f"Other Bank Charges set to RTGS: {rtgs_charge}%, IMPS: {imps_charge}%"

    def see_service_charges(self):
        print(f"Same Bank Charges: RTGS: {self._same_bank_charges['RTGS']}%, IMPS: {self._same_bank_charges['IMPS']}%")
        print(f"Other Bank Charges: RTGS: {self._other_bank_charges['RTGS']}%, IMPS: {self._other_bank_charges['IMPS']}%")

    def revert_transaction(self, account_id, txn_id):
        if account_id not in self._accounts:
            return "Account not found."

        account = self._accounts[account_id]
        for txn in account.get_transactions():
            if txn.get_txn_id() == txn_id:
                if txn.get_txn_type() == "Deposit":
                    if account.get_balance() - txn.get_amount() < 0:
                        return "Cannot revert transaction: Account balance would go negative."
                    account._balance -= txn.get_amount()
                elif txn.get_txn_type() == "Withdraw":
                    account._balance += txn.get_amount()
                elif txn.get_txn_type() == "Transfer Out":
                    receiver_id = txn.get_details()["receiver_id"]
                    amount = txn.get_amount()
                    if receiver_id in self._accounts:
                        if self._accounts[receiver_id].get_balance() - amount < 0:
                            return "Cannot revert transaction: Receiver's balance would go negative."
                        account._balance += amount
                        self._accounts[receiver_id]._balance -= amount
                        for txn_receiver in self._accounts[receiver_id].get_transactions():
                            if txn_receiver.get_txn_type() == "Transfer In" and txn_receiver.get_amount() == amount:
                                self._accounts[receiver_id]._transactions.remove(txn_receiver)
                                break
                elif txn.get_txn_type() == "Transfer In":
                    sender_id = txn.get_details()["sender_id"]
                    amount = txn.get_amount()
                    if sender_id in self._accounts:
                        if self._accounts[sender_id].get_balance() - amount < 0:
                            return "Cannot revert transaction: Sender's balance would go negative."
                        account._balance -= amount
                        self._accounts[sender_id]._balance += amount
                        for txn_sender in self._accounts[sender_id].get_transactions():
                            if txn_sender.get_txn_type() == "Transfer Out" and txn_sender.get_amount() == amount:
                                self._accounts[sender_id]._transactions.remove(txn_sender)
                                break

                account._transactions.remove(txn)
                self.save_to_json()
                return f"Transaction {txn_id} reverted successfully!"
        return "Transaction not found."
    def deposit(self, account_id, amount, currency):
        if account_id not in self._accounts:
            return "Account not found."
        if currency not in self._accepted_currencies:
            return f"Currency {currency} not accepted."
        if amount <= 0:
            return "Amount must be greater than zero."
        result = self._accounts[account_id].deposit(amount, currency, self._accepted_currencies[currency])
        self.save_to_json()
        return result

    def withdraw(self, account_id, amount):
        if account_id not in self._accounts:
            return "Account not found."
        if amount <= 0:
            return "Amount must be greater than zero."
        result = self._accounts[account_id].withdraw(amount)
        self.save_to_json()
        return result

    def transfer(self, sender_id, receiver_id, amount, same_bank=True):
        if sender_id not in self._accounts:
            return "Sender account not found."
        if receiver_id not in self._accounts:
            return "Receiver account not found."
        if amount <= 0:
            return "Amount must be greater than zero."

        # Confirmation prompt
        confirm = input(f"Are you sure you want to transfer {amount} INR from {sender_id} to {receiver_id}? (yes/no): ").lower()
        if confirm != "yes":
            return "Transfer cancelled."

        charge = self._same_bank_charges["RTGS"] if same_bank else self._other_bank_charges["RTGS"]
        total_deduction = amount + (amount * charge / 100)

        if self._accounts[sender_id].get_balance() >= total_deduction:
            self._accounts[sender_id]._balance -= total_deduction
            self._accounts[receiver_id]._balance += amount
            txn_id_sender = f"TXN{self._bank_id}{sender_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            txn_id_receiver = f"TXN{self._bank_id}{receiver_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            self._accounts[sender_id]._transactions.append(Transaction(txn_id_sender, sender_id, "Transfer Out", amount, receiver_id=receiver_id))
            self._accounts[receiver_id]._transactions.append(Transaction(txn_id_receiver, receiver_id, "Transfer In", amount, sender_id=sender_id))
            self.save_to_json()
            return f"{amount} INR transferred from {sender_id} to {receiver_id} (charges: {charge}%)"
        return "Insufficient balance!"

    def get_account_balance(self, account_id):
        if account_id in self._accounts:
            return f"Balance: {self._accounts[account_id].get_balance()} INR"
        return "Account not found."

    def view_all_transactions(self):
        transactions = []
        for account in self._accounts.values():
            transactions.extend(account.get_transactions())
        return "\n".join(str(txn) for txn in transactions) if transactions else "No transactions found."


def main():
    bank = Bank("SBI")

    while True:
        print("\n1. Login as Bank Staff")
        print("2. Login as Account Holder")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username == "admin" and password == "admin123":
                while True:
                    print("\nBank Staff Menu:")
                    print("1. Create Account")
                    print("2. Update Account")
                    print("3. Delete Account")
                    print("4. Add Currency")
                    print("5. Set Same Bank Charges")
                    print("6. Set Other Bank Charges")
                    print("7. View All Transactions")
                    print("8. Revert Transaction")
                    print("9. See All Currency Details")
                    print("10. See Transaction Charges")
                    print("11. Logout")

                    option = input("Enter option: ")
                    if option == "1":
                        name = input("Enter Account Holder Name: ")
                        print(bank.create_account(name))
                    elif option == "2":
                        account_id = input("Enter Account ID: ")
                        new_name = input("Enter New Name: ")
                        print(bank.update_account(account_id, new_name))
                    elif option == "3":
                        account_id = input("Enter Account ID: ")
                        print(bank.delete_account(account_id))
                    elif option == "4":
                        currency = input("Enter Currency: ")
                        exchange_rate = float(input("Enter Exchange Rate: "))
                        print(bank.add_currency(currency, exchange_rate))
                    elif option == "5":
                        rtgs_charge = float(input("Enter RTGS charge for same bank: "))
                        imps_charge = float(input("Enter IMPS charge for same bank: "))
                        print(bank.set_charges(rtgs_charge, imps_charge, same_bank=True))
                    elif option == "6":
                        rtgs_charge = float(input("Enter RTGS charge for other bank: "))
                        imps_charge = float(input("Enter IMPS charge for other bank: "))
                        print(bank.set_charges(rtgs_charge, imps_charge, same_bank=False))
                    elif option == "7":
                        print(bank.view_all_transactions())
                    elif option == "8":
                        account_id = input("Enter Account ID: ")
                        txn_id = input("Enter Transaction ID: ")
                        print(bank.revert_transaction(account_id, txn_id))
                    elif option == "9":
                        bank.display_currency_details()
                    elif option == "10":
                        bank.see_service_charges()
                    elif option == "11":
                        break
            else:
                print("Invalid username or password")
        elif choice == "2":
            account_id = input("Enter Your Username: ")
            password = input("Enter Password: ")
            if account_id in bank.get_accounts() and bank.get_accounts()[account_id].verify_password(password):
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer Funds")
                    print("4. Check Balance")
                    print("5. View Transaction History")
                    print("6. Logout")

                    option = input("Enter option: ")
                    if option == "1":
                        amount = float(input("Enter amount: "))
                        currency = input("Enter currency (INR by default): ")
                        print(bank.deposit(account_id, amount, currency))
                    elif option == "2":
                        amount = float(input("Enter amount: "))
                        print(bank.withdraw(account_id, amount))
                    elif option == "3":
                        receiver_id = input("Enter receiver Account ID: ")
                        amount = float(input("Enter amount: "))
                        same_bank = input("Is the receiver in the same bank? (yes/no): ").lower() == "yes"
                        print(bank.transfer(account_id, receiver_id, amount, same_bank))
                    elif option == "4":
                        print(bank.get_account_balance(account_id))
                    elif option == "5":
                        print(bank.get_accounts()[account_id].get_transaction_history())
                    elif option == "6":
                        break
            else:
                print("Invalid account ID or password")
        elif choice == "3":
            break


if __name__ == "__main__":
    main()