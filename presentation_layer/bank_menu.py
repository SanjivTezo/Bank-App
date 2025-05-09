from models.bank import Bank
from data_access_layer.bank_repo import save_bank_data  # Import save_bank_data from the data access layer

def create_new_bank():
    bank_name = input("Enter Bank Name: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    bank = Bank(bank_name, username, password)  
    save_bank_data(bank)  

    print(f"Bank {bank_name} created successfully.")
    return bank