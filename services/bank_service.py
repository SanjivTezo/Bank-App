import json
from utils.helpers import load_json_data
from models.getters.BankGetters import BankGetters 
from data_access_layer.bank_repo import save_charges  
from data_access_layer.bank_repo import save_accepted_currencies  

def add_currency(bank, currency, exchange_rate):
    bank_getters = BankGetters(bank)  
    bank_id = bank_getters.get_bank_id()  

    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        accepted_currencies = all_data.get("accepted_currencies", [])
        for entry in accepted_currencies:
            if entry["bank_id"] == bank_id:
                entry["accepted_currencies"][currency] = exchange_rate

                save_accepted_currencies(accepted_currencies)

                return f"{currency} added with exchange rate {exchange_rate}"

        return "Bank not found in accepted_currencies section."
    return "Data file not found."




def set_charges(bank, rtgs_charge, imps_charge, same_bank=True):
    bank_getters = BankGetters(bank)  
    bank_id = bank_getters.get_bank_id() 

    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        charges = all_data.get("charges", [])
        for entry in charges:
            if entry["bank_id"] == bank_id:
                if same_bank:
                    entry["same_bank_charges"] = {"RTGS": rtgs_charge, "IMPS": imps_charge}
                else:
                    entry["other_bank_charges"] = {"RTGS": rtgs_charge, "IMPS": imps_charge}

                save_charges(charges)

                return f"Charges updated successfully! RTGS: {rtgs_charge}%, IMPS: {imps_charge}%"

        return "Bank not found in charges section."
    return "Data file not found."
