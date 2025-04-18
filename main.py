from models.bank import Bank
import os
import json
from services.account_service import AccountService
from services.transaction_service import TransactionService
from services.bank_service import BankService

def main():
    print("Welcome to the Banking System")
    bank = None

    while True:
        print("\n1. Create New Bank ")
        print("2. Login as Bank Staff")
        print("3. Login as Account Holder")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            bank_name = input("Enter Bank Name: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            bank = Bank(bank_name, username, password)
            bank.save_to_json()
            # account_service = AccountService(bank)
            # transaction_service = TransactionService(bank)
            # bank_service = BankService(bank)
            print(f"Bank {bank_name} created successfully.")

        elif choice == "2":
            if os.path.exists("data/bank_data.json"):
                with open("data/bank_data.json", "r") as file:
                     all_banks = json.load(file)
                bank_name = input("Enter Bank Name: ")
                if bank_name not in all_banks:
                    print("Bank Does Not Exits")
                    continue
                bank_data = all_banks[bank_name]
                bank = Bank(bank_data["name"], bank_data["admin_user"], bank_data["admin_pass"])
                account_service = AccountService(bank)
                transaction_service = TransactionService(bank)
                bank_service = BankService(bank)
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username == bank.get_username() and password == bank.get_password():
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
                        print(account_service.create_account(name))
                    elif option == "2":
                        account_id = input("Enter Account ID: ")
                        new_name = input("Enter New Name: ")
                        print(account_service.update_account(account_id, new_name))
                    elif option == "3":
                        account_id = input("Enter Account ID: ")
                        print(account_service.delete_account(account_id))
                    elif option == "4":
                        currency = input("Enter Currency: ")
                        exchange_rate = float(input("Enter Exchange Rate: "))
                        print(bank_service.add_currency(currency, exchange_rate))
                    elif option == "5":
                        rtgs_charge = float(input("Enter RTGS charge for same bank: "))
                        imps_charge = float(input("Enter IMPS charge for same bank: "))
                        print(bank_service.set_charges(rtgs_charge, imps_charge, same_bank=True))
                    elif option == "6":
                        rtgs_charge = float(input("Enter RTGS charge for other bank: "))
                        imps_charge = float(input("Enter IMPS charge for other bank: "))
                        print(bank_service.set_charges(rtgs_charge, imps_charge, same_bank=False))
                    elif option == "7":
                        print(transaction_service.view_all_transactions())
                    elif option == "8":
                        account_id = input("Enter Account ID: ")
                        txn_id = input("Enter Transaction ID: ")
                        print(transaction_service.revert_transaction(account_id, txn_id))
                    elif option == "9":
                        print(bank_service.display_currency_details())
                    elif option == "10":
                        print(bank_service.see_service_charges())
                    elif option == "11":
                        break
            else:
                print("Invalid username or password")
        elif choice == "3":
            if os.path.exists("data/bank_data.json"):
                with open("data/bank_data.json", "r") as file:
                    all_banks = json.load(file)
                bank_name = input("Enter Bank Name: ")
                if bank_name not in all_banks:
                    print("Bank Does Not Exist. Please create it first (option 1) or login as staff.")
                    continue
                # build the Bank instance and its services
                bank_data = all_banks[bank_name]
                bank = Bank(bank_data["name"],
                            bank_data["admin_user"],
                            bank_data["admin_pass"])
                account_service = AccountService(bank)
                transaction_service = TransactionService(bank)
            else:
                print("No banks available. Please create a bank first.")
                continue
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
                        print(transaction_service.deposit(account_id, amount, currency))
                    elif option == "2":
                        amount = float(input("Enter amount: "))
                        print(transaction_service.withdraw(account_id, amount))
                    elif option == "3":
                        receiver_id = input("Enter receiver Account ID: ")
                        amount = float(input("Enter amount: "))
                        same_bank = input("Is the receiver in the same bank? (yes/no): ").lower() == "yes"
                        print(transaction_service.transfer(account_id, receiver_id, amount, same_bank))
                    elif option == "4":
                        print(account_service.get_account_balance(account_id))
                    elif option == "5":
                        print(bank.get_accounts()[account_id].get_transaction_history())
                    elif option == "6":
                        break
            else:
                print("Invalid account ID or password")
        elif choice == "4":
            break

if __name__ == "__main__":
    main()