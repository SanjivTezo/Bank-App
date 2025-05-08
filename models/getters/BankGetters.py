class BankGetters:
    def __init__(self, bank):
        self._bank = bank
    def get_bank_id(self):
        return self._bank.get_bank_id()  

    def get_accepted_currencies(self):
        return self._bank.get_accepted_currencies()

    def get_accounts(self):
        return self._bank._accounts 
    
    def get_username(self):
        return self._bank._admin_user  

    def get_password(self):
        return self._bank._admin_pass 