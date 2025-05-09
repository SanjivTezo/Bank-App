from utils.helpers import save_to_json

def save_transaction(transaction):

    save_to_json("data/bank_data.json", "transactions", transaction)