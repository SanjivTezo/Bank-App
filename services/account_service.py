from account import Account

class AccountService:
    def __init__(self, bank):
        self.bank = bank
        
        

    def create_account(self, name):
        account = Account(name, self.bank.get_bank_id())
        self.bank.get_accounts()[account.get_account_id()] = account
        self.bank.save_to_json()
        return f"Account created! ID: {account.get_account_id()}, Password: {account._password}"

    def update_account(self, account_id, new_name):
        if account_id in self.bank.get_accounts():
            old_name = self.bank.get_accounts()[account_id].get_name()
            self.bank.get_accounts()[account_id]._name = new_name
            self.bank.save_to_json()
            return f"Account {account_id} updated from {old_name} to {new_name} successfully!"
        return "Account not found."

    def delete_account(self, account_id):
        if account_id in self.bank.get_accounts():
            del self.bank.get_accounts()[account_id]
            self.bank.save_to_json()
            return "Account deleted successfully!"
        return "Account not found."

    def get_account_balance(self, account_id):
        if account_id in self.bank.get_accounts():
            return f"Balance: {self.bank.get_accounts()[account_id].get_balance()} INR"
        return "Account not found."