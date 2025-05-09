import os
import json
from services.account_service import update_account, delete_account
from services.bank_service import add_currency, set_charges
from services.transaction_service import view_all_transactions, revert_transaction
from models.account import Account
from utils.json_utils import save_to_json
from utils.helpers import load_json_data
from data_access_layer.account_repo import save_account  # Import save_account from the data access layer
from models.getters.BankGetters import BankGetters  # Import BankGetters

def create_account_action(bank):
    name = input("Enter Account Holder Name: ")
    bank_getters = BankGetters(bank) 
    bank_id = bank_getters.get_bank_id() 
    account = Account(name, bank_id)  
    save_account(account.to_dict())  
    print(f"Account created! ID: {account._account_id}, Password: {account._password}")

def update_account_action(bank):
    account_id = input("Enter Account ID: ")
    new_name = input("Enter New Name: ")
    result = update_account(bank, account_id, new_name)
    print(result)

def delete_account_action(bank):
    account_id = input("Enter Account ID: ")
    result = delete_account(bank, account_id)
    print(result)

def add_currency_action(bank):
    currency = input("Enter Currency: ")
    exchange_rate = float(input("Enter Exchange Rate: "))
    result = add_currency(bank, currency, exchange_rate)
    print(result)

def set_same_bank_charges_action(bank):
    rtgs_charge = float(input("Enter RTGS charge for same bank: "))
    imps_charge = float(input("Enter IMPS charge for same bank: "))
    result = set_charges(bank, rtgs_charge, imps_charge, same_bank=True)
    print(result)

def set_other_bank_charges_action(bank):
    rtgs_charge = float(input("Enter RTGS charge for other bank: "))
    imps_charge = float(input("Enter IMPS charge for other bank: "))
    result = set_charges(bank, rtgs_charge, imps_charge, same_bank=False)
    print(result)

def view_all_transactions_action(bank):
    print(view_all_transactions(bank))

def revert_transaction_action(bank):
    account_id = input("Enter Account ID: ")
    txn_id = input("Enter Transaction ID: ")
    result = revert_transaction(bank, account_id, txn_id)
    print(result)

def display_currency_details_action(bank):
    bank_getters = BankGetters(bank) 
    bank_id = bank_getters.get_bank_id()  
    bank_name = bank_getters.get_bank_name()  

    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        accepted_currencies = all_data.get("accepted_currencies", [])
        for entry in accepted_currencies:
            if entry["bank_id"] == bank_id:
                print(f"Accepted Currencies for {bank_name}: {entry['accepted_currencies']}")
                return

        print("No currency details found for this bank.")

def see_service_charges_action(bank):
    bank_getters = BankGetters(bank) 
    bank_id = bank_getters.get_bank_id()  

    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        charges = all_data.get("charges", [])
        for entry in charges:
            if entry["bank_id"] == bank_id:
                print(f"Same Bank Charges: {entry['same_bank_charges']}")
                print(f"Other Bank Charges: {entry['other_bank_charges']}")
                return

        print("No charges found for this bank.")