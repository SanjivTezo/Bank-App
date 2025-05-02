from services.account_service import create_account, update_account, delete_account
from services.bank_service import add_currency, set_charges, see_service_charges, display_currency_details
from services.transaction_service import view_all_transactions, revert_transaction

def create_account_action(bank):
    name = input("Enter Account Holder Name: ")
    print(create_account(bank, name))

def update_account_action(bank):
    account_id = input("Enter Account ID: ")
    new_name = input("Enter New Name: ")
    print(update_account(bank, account_id, new_name))

def delete_account_action(bank):
    account_id = input("Enter Account ID: ")
    print(delete_account(bank, account_id))

def add_currency_action(bank):
    currency = input("Enter Currency: ")
    exchange_rate = float(input("Enter Exchange Rate: "))
    print(add_currency(bank, currency, exchange_rate))

def set_same_bank_charges_action(bank):
    rtgs_charge = float(input("Enter RTGS charge for same bank: "))
    imps_charge = float(input("Enter IMPS charge for same bank: "))
    print(set_charges(bank, rtgs_charge, imps_charge, same_bank=True))

def set_other_bank_charges_action(bank):
    rtgs_charge = float(input("Enter RTGS charge for other bank: "))
    imps_charge = float(input("Enter IMPS charge for other bank: "))
    print(set_charges(bank, rtgs_charge, imps_charge, same_bank=False))

def view_all_transactions_action(bank):
    print(view_all_transactions(bank))

def revert_transaction_action(bank):
    account_id = input("Enter Account ID: ")
    txn_id = input("Enter Transaction ID: ")
    print(revert_transaction(bank, account_id, txn_id))

def display_currency_details_action(bank):
    print(display_currency_details(bank))

def see_service_charges_action(bank):
    charges = see_service_charges(bank)
    print("Same Bank Charges:", charges["same_bank"])
    print("Other Bank Charges:", charges["other_bank"])