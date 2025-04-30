from models.bank import Bank
import os
import json
from services.account_service import create_account, update_account, delete_account, get_account_balance
from services.transaction_service import deposit, withdraw, transfer, revert_transaction, view_all_transactions
from services.bank_service import add_currency, set_charges, see_service_charges, display_currency_details
from utils.json_utils import save_to_json, load_from_json
from utils.getters import BankGetters, AccountGetters, TransactionGetters


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
            save_to_json("data/bank_data.json", bank_name, bank.to_dict())
            print(f"Bank {bank_name} created successfully.")

        elif choice == "2":
            if os.path.exists("data/bank_data.json"):
                with open("data/bank_data.json", "r") as file:
                    all_banks = json.load(file)
                bank_name = input("Enter Bank Name: ")
                if bank_name not in all_banks:
                    print("Bank Does Not Exist")
                    continue
                bank_data = all_banks[bank_name]
                # Create the Bank instance which will load its own data
                bank = Bank(bank_data["name"], bank_data["admin_user"], bank_data["admin_pass"])
                bank_getters = BankGetters(bank)

                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if username == bank_getters.get_username() and password == bank_getters.get_password():
            # Rest of the bank staff menu code...
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
                            print(create_account(bank, name))
                        elif option == "2":
                            account_id = input("Enter Account ID: ")
                            new_name = input("Enter New Name: ")
                            print(update_account(bank, account_id, new_name))
                        elif option == "3":
                            account_id = input("Enter Account ID: ")
                            print(delete_account(bank, account_id))
                        elif option == "4":
                            currency = input("Enter Currency: ")
                            exchange_rate = float(input("Enter Exchange Rate: "))
                            print(add_currency(bank, currency, exchange_rate))  # Pass the bank object explicitly
                        elif option == "5":
                            rtgs_charge = float(input("Enter RTGS charge for same bank: "))
                            imps_charge = float(input("Enter IMPS charge for same bank: "))
                            print(set_charges(bank, rtgs_charge, imps_charge, same_bank=True))  # Pass the bank object explicitly

                        elif option == "6":
                            rtgs_charge = float(input("Enter RTGS charge for other bank: "))
                            imps_charge = float(input("Enter IMPS charge for other bank: "))
                            print(set_charges(bank, rtgs_charge, imps_charge, same_bank=False))  # Pass the bank object explicitly

                        elif option == "7":
                            print(view_all_transactions(bank))  # Pass the bank object explicitly
                        elif option == "8":
                            account_id = input("Enter Account ID: ")
                            txn_id = input("Enter Transaction ID: ")
                            print(revert_transaction(bank, account_id, txn_id))
                        elif option == "9":
                            print(display_currency_details(bank))  # Pass the bank object explicitly
                        elif option == "10":
                            charges = see_service_charges(bank)  # Pass the bank object explicitly
                            print("Same Bank Charges:", charges["same_bank"])
                            print("Other Bank Charges:", charges["other_bank"])
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
                bank_data = all_banks[bank_name]
                bank = Bank(bank_data["name"], bank_data["admin_user"], bank_data["admin_pass"])
                bank_getters = BankGetters(bank)  # Instantiate BankGetters
            else:
                print("No banks available. Please create a bank first.")
                continue
            account_id = input("Enter Your Username: ")
            password = input("Enter Password: ")
            if account_id in bank_getters.get_accounts():
                account = bank_getters.get_accounts()[account_id]
                account_getters = AccountGetters(account)  # Instantiate AccountGetters
                if account_getters.verify_password(password):  # Use AccountGetters to verify the password
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
                            print(deposit(bank, account_id, amount, currency))  # Pass the bank object explicitly
                        elif option == "2":
                            amount = float(input("Enter amount: "))
                            print(withdraw(bank, account_id, amount))
                        elif option == "3":
                            receiver_id = input("Enter receiver Account ID: ")
                            amount = float(input("Enter amount: "))
                            same_bank = input("Is the receiver in the same bank? (yes/no): ").lower() == "yes"
                            print(transfer(bank, account_id, receiver_id, amount, same_bank))
                        elif option == "4":
                            print(get_account_balance(bank, account_id))  # Pass the bank object explicitly
                        elif option == "5":
                            transactions = account_getters.get_transactions_string()  # Get formatted transactions
                            print("\n".join(transactions))  # Print each transaction on a new line
                        elif option == "6":
                            break
                else:
                    print("Invalid password")
            else:
                print("Invalid account ID")
        elif choice == "4":
            break


if __name__ == "__main__":
    main()