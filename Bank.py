import datetime
import random

class Transaction:
    def __init__(self, txn_id, account_id, txn_type, amount, **kwargs):
        self.txn_id = txn_id
        self.account_id = account_id
        self.txn_type = txn_type
        self.amount = amount
        self.details = kwargs
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"Transaction[ID: {self.txn_id}, Type: {self.txn_type}, Amount: {self.amount}, Details: {self.details}, Timestamp: {self.timestamp}]"


class Account:
    def __init__(self, name):
        self.account_id = name[:3].upper() + datetime.datetime.now().strftime("%Y%m%d")
        self.name = name
        self.password = str(random.randint(1000, 9999))
        self.balance = 0
        self.transactions = []

    def deposit(self, amount, currency, exchange_rate):
        converted_amount = amount * exchange_rate
        self.balance += converted_amount
        txn_id = f"TXN{self.account_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        txn = Transaction(txn_id, self.account_id, "Deposit", converted_amount, currency=currency)
        self.transactions.append(txn)
        return f"Deposited {converted_amount} INR to {self.account_id} successfully!"

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            txn_id = f"TXN{self.account_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            txn = Transaction(txn_id, self.account_id, "Withdraw", amount)
            self.transactions.append(txn)
            return f"Withdrawn {amount} INR from {self.account_id} successfully!"
        return "Insufficient balance!"

    def get_transaction_history(self):
        return "\n".join(str(txn) for txn in self.transactions) if self.transactions else "No transactions found."

    def __str__(self):
        return f"Account[ID: {self.account_id}, Name: {self.name}, Balance: {self.balance}]"


class Bank:
    def __init__(self, name):
        self.name = name
        self.bank_id = name[:3].upper() + datetime.datetime.now().strftime("%Y%m%d")
        # self.rtgs_charges = {"same_bank": 0, "other_bank": 2}
        # self.imps_charges = {"same_bank": 5, "other_bank": 6}

        self.same_bank_charges = {"RTGS": 0, "IMPS": 5}
        self.other_bank_charges = {"RTGS": 2, "IMPS": 6}
        self.accepted_currencies = {"INR": 1}
        self.accounts = {}

    def create_account(self, name):
        account = Account(name)
        self.accounts[account.account_id] = account
        return f"Account created! ID: {account.account_id}, Password: {account.password}"

    def update_account(self, account_id, new_name):
        if account_id in self.accounts:
            old_name=self.accounts[account_id].name
            self.accounts[account_id].name = new_name
            return f"Account {account_id} updated  form {old_name} to {new_name} successfully!"
        return "Account not found."

    def delete_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            return "Account deleted successfully!"
        return "Account not found."

    def add_currency(self, currency, exchange_rate):
        self.accepted_currencies[currency] = exchange_rate
        return f"{currency} added with exchange rate {exchange_rate}"
    
    def display_currency_details(self):
        if not self.accepted_currencies:
            print("\nNo currencies available.")
            return
        print("\nAll Currency Details:")
        for currency, exchange_rate in self.accepted_currencies.items():
            print(f"{currency}: {exchange_rate}")
    
    def set_same_bank_charges(self, rtgs_charge, imps_charge):
        self.same_bank_charges={"RTGS":rtgs_charge, "IMPS":imps_charge}
        return f"Same Bank Charges set to RTGS: {rtgs_charge}%, IMPS: {imps_charge}%"
    
    def set_other_bank_charges(self, rtgs_charge, imps_charge):
        self.other_bank_charges={"RTGS":rtgs_charge, "IMPS":imps_charge}
        return f"Other Bank Charges set to RTGS: {rtgs_charge}%, IMPS: {imps_charge}%"
    
    def see_service_charges(self):
        print(f"Same Bank Charges: RTGS: {self.same_bank_charges['RTGS']}%, IMPS: {self.same_bank_charges['IMPS']}%")
        print(f"Other Bank Charges: RTGS: {self.other_bank_charges['RTGS']}%, IMPS: {self.other_bank_charges['IMPS']}%")

    def revert_transaction(self, account_id, txn_id):
        if account_id in self.accounts:
            for txn in self.accounts[account_id].transactions:
                if txn.txn_id == txn_id:
                    if txn.txn_type == "Deposit":
                        self.accounts[account_id].balance -= txn.amount
                    elif txn.txn_type == "Withdraw":
                        self.accounts[account_id].balance += txn.amount
                    self.accounts[account_id].transactions.remove(txn)
                    return f"Transaction {txn_id} reverted successfully!"
            return "Transaction not found."
        return "Account not found."


    def deposit(self, account_id, amount, currency):
        if account_id in self.accounts and currency in self.accepted_currencies:
            return self.accounts[account_id].deposit(amount, currency, self.accepted_currencies[currency])
        return "Invalid account or currency."

    def withdraw(self, account_id, amount):
        if account_id in self.accounts:
            return self.accounts[account_id].withdraw(amount)
        return "Account not found."

    def transfer(self, sender_id, receiver_id, amount, same_bank=True):
        if sender_id in self.accounts and receiver_id in self.accounts:
            # charge = self.rtgs_charges["same_bank"] if same_bank else self.rtgs_charges["other_bank"]
            charge = self.same_bank_charges["RTGS"] if same_bank else self.other_bank_charges["RTGS"]


            total_deduction = amount + (amount * charge / 100)

            if self.accounts[sender_id].balance >= total_deduction:
                self.accounts[sender_id].balance -= total_deduction
                self.accounts[receiver_id].balance += amount
                txn_id_sender = f"TXN{sender_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                txn_id_receiver = f"TXN{receiver_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.accounts[sender_id].transactions.append(Transaction(txn_id_sender, sender_id, "Transfer Out", amount))
                self.accounts[receiver_id].transactions.append(Transaction(txn_id_receiver, receiver_id, "Transfer In", amount))
                return f"{amount} INR transferred from {sender_id} to {receiver_id} (charges: {charge}%)"
            return "Insufficient balance!"
        return "Invalid account details."

    def get_account_balance(self, account_id):
        if account_id in self.accounts:
            return f"Balance: {self.accounts[account_id].balance} INR"
        return "Account not found."

    def view_all_transactions(self):
        transactions = []
        for account in self.accounts.values():
            transactions.extend(account.transactions)
        return "\n".join(str(txn) for txn in transactions) if transactions else "No transactions found."


def main():
    bank = Bank("SBI")
    
    while True:
        print("\n1. Login as Bank Staff")
        print("2. Login as Account Holder")
        print("3. Exit")

        choice = input("Enter your choice:")
        if choice == "1":
            password = input("Enter your staff password:")
            if password == "a":
                while True:
                    print("\nBank Staff Menu:")
                    print("1. Create Account")
                    print("2. Update Account")
                    print("3. Delete Account")
                    print("4. Add Currency")
                    print("5. Add Service Charges For Same Bank")
                    print("6. Add Service Charges For Other Bank")
                    print("7. View All Transactions")
                    print("8. Revert Transaction")

                    print("9. See All Currency Details")
                    print("10. See Transaction Charges")
                    print("11. Logout")

                    option = input("Enter option: ")
                    if option == "1":
                        name = input("Enter Account Holder Name:")
                        print(bank.create_account(name))

                    elif option == "2":
                        account_id = input("Enter Account ID:")
                        new_name = input("Enter New Name:")
                        print(bank.update_account(account_id, new_name))

                    elif option == "3":
                        account_id = input("Enter Account ID:")
                        print(bank.delete_account(account_id))

                    elif option == "4":
                        currency = input("Enter Currency:")
                        exchange_rate = float(input("Enter Exchange Rate:"))
                        print(bank.add_currency(currency, exchange_rate))

                    elif option == "5":
                        rtgs_charge = float(input("Enter RTGS charge for same bank: "))
                        imps_charge = float(input("Enter IMPS charge for same bank: "))
                        print(bank.set_same_bank_charges(rtgs_charge, imps_charge))

                    elif option == "6":
                        rtgs_charge = float(input("Enter RTGS charge for other bank: "))
                        imps_charge = float(input("Enter IMPS charge for other bank: "))
                        print(bank.set_other_bank_charges(rtgs_charge, imps_charge))

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
        elif choice == "2":
            account_id = input("Enter Account ID:")
            password = input("Enter Password:")
            if account_id in bank.accounts and bank.accounts[account_id].password == password:
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
                        print(bank.accounts[account_id].get_transaction_history())
                    elif option == "6":
                        break

        elif choice == "3":
            break

if __name__ == "__main__":
    main()

