from models.bank import Bank
from utils.json_utils import save_to_json

def create_new_bank():
    bank_name = input("Enter Bank Name: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    bank = Bank(bank_name, username, password)
    save_to_json("data/bank_data.json", bank_name, bank.to_dict())
    print(f"Bank {bank_name} created successfully.")
    return bank