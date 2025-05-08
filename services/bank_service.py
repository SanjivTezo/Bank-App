import json
from utils.helpers import  load_json_data

def add_currency(bank, currency, exchange_rate):
    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        accepted_currencies = all_data.get("accepted_currencies", [])
        for entry in accepted_currencies:
            if entry["bank_id"] == bank._bank_id:
                entry["accepted_currencies"][currency] = exchange_rate

                with open(file_path, "w") as file:
                    json.dump(all_data, file, indent=4)

                return f"{currency} added with exchange rate {exchange_rate}"

        return "Bank not found in accepted_currencies section."
    return "Data file not found."

def set_charges(bank, rtgs_charge, imps_charge, same_bank=True):
    file_path = "data/bank_data.json"
    all_data = load_json_data(file_path)

    if all_data:
        charges = all_data.get("charges", [])
        for entry in charges:
            if entry["bank_id"] == bank._bank_id:
                if same_bank:
                    entry["same_bank_charges"] = {"RTGS": rtgs_charge, "IMPS": imps_charge}
                else:
                    entry["other_bank_charges"] = {"RTGS": rtgs_charge, "IMPS": imps_charge}

                with open(file_path, "w") as file:
                    json.dump(all_data, file, indent=4)

                return f"Charges updated successfully! RTGS: {rtgs_charge}%, IMPS: {imps_charge}%"

        return "Bank not found in charges section."
    return "Data file not found."

def see_service_charges(bank):
    return {
        "same_bank": bank._same_bank_charges,
        "other_bank": bank._other_bank_charges
    }

def display_currency_details(bank):
    return bank._accepted_currencies