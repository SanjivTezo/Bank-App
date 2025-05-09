from utils.json_utils import save_to_json

def save_bank_data(bank):

    save_to_json("data/bank_data.json", "bank", bank.to_dict())
    save_to_json("data/bank_data.json", "charges", bank.to_charges_dict())
    save_to_json("data/bank_data.json", "accepted_currencies", bank.to_accepted_currencies_dict())

def save_charges(charges):
    save_to_json("data/bank_data.json", "charges", charges)

def save_accepted_currencies(accepted_currencies):
    save_to_json("data/bank_data.json", "accepted_currencies", accepted_currencies)


