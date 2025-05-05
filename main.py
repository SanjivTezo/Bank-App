from models.bank import Bank
import os
import json
from utils.getters import BankGetters, AccountGetters
from presentation_layer.bank_menu import create_new_bank
from presentation_layer.staff_actions import (
    create_account_action, update_account_action, delete_account_action,
    add_currency_action, set_same_bank_charges_action, set_other_bank_charges_action,
    view_all_transactions_action, revert_transaction_action, display_currency_details_action,
    see_service_charges_action
)
from presentation_layer.account_holder_actions import (
    deposit_action, withdraw_action, transfer_action,
    check_balance_action, view_transaction_history_action
)

from presentation_layer.staff_menu import display_staff_menu
from presentation_layer.account_holder_menu import display_account_holder_menu
from utils.helpers import load_bank

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
            create_new_bank()
        elif choice == "2":
            bank_name = input("Enter Bank Name: ")
            bank, error = load_bank("data/bank_data.json", bank_name)
            if error:
                print(error)
                continue
            bank_getters = BankGetters(bank)

            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username == bank_getters.get_username() and password == bank_getters.get_password():
                while True:
                    display_staff_menu()

                    option = input("Enter option: ")
                    if option == "1":
                        create_account_action(bank)
                    elif option == "2":
                        update_account_action(bank)
                    elif option == "3":
                        delete_account_action(bank)
                    elif option == "4":
                        add_currency_action(bank)
                    elif option == "5":
                        set_same_bank_charges_action(bank)
                    elif option == "6":
                        set_other_bank_charges_action(bank)
                    elif option == "7":
                        view_all_transactions_action(bank)
                    elif option == "8":
                        revert_transaction_action(bank)
                    elif option == "9":
                        display_currency_details_action(bank)
                    elif option == "10":
                        see_service_charges_action(bank)
                    elif option == "11":
                        break
            else:
                print("Invalid username or password")
        elif choice == "3":
            bank_name = input("Enter Bank Name: ")
            bank, error = load_bank("data/bank_data.json", bank_name)
            if error:
                print(error)
                continue

            account_id = input("Enter Your Username: ")
            password = input("Enter Password: ")

            # Check if the account exists in the bank's accounts
            if account_id in bank._accounts:
                account = bank._accounts[account_id]
                if account["account_password"] == password:
                    print(f"Welcome, {account['account_name']}!")
                    while True:
                        display_account_holder_menu()
                        option = input("Enter option: ")
                        if option == "1":
                            deposit_action(bank, account_id)
                        elif option == "2":
                            withdraw_action(bank, account_id)
                        elif option == "3":
                            transfer_action(bank, account_id)
                        elif option == "4":
                            check_balance_action(bank, account_id)
                        elif option == "5":
                            view_transaction_history_action(bank, account_id)
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