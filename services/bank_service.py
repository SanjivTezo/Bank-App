from models.bank import Bank
from models.account import Account
from models.transaction import Transaction
from utils.getters import AccountGetters, BankGetters, TransactionGetters
from utils.helpers import save_bank_data

def add_currency(bank, currency, exchange_rate):
    bank._accepted_currencies[currency] = exchange_rate
    save_bank_data(bank)  
    return f"{currency} added with exchange rate {exchange_rate}"

def set_charges(bank, rtgs_charge, imps_charge, same_bank=True):
    if same_bank:
        bank._same_bank_charges = {"RTGS": rtgs_charge, "IMPS": imps_charge}
    else:
        bank._other_bank_charges = {"RTGS": rtgs_charge, "IMPS": imps_charge}
    
    save_bank_data(bank)  
    return f"Charges updated successfully! RTGS: {rtgs_charge}%, IMPS: {imps_charge}%"

def see_service_charges(bank):
    return {
        "same_bank": bank._same_bank_charges,
        "other_bank": bank._other_bank_charges
    }

def display_currency_details(bank):
    return bank._accepted_currencies