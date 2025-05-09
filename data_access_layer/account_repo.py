from utils.helpers import save_to_json

def save_account(account):
    save_to_json("data/bank_data.json", "accounts", account)


def save_all_accounts(accounts):
    save_to_json("data/bank_data.json", "accounts", accounts)