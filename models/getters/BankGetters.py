class BankGetters:
    def __init__(self, bank):
        self._bank = bank
    def get_bank_id(self):
         return self._bank._bank_id 

    def get_accepted_currencies(self):
        return self._bank._accepted_currencies

    def get_accounts(self):
        return self._bank._accounts 
    
    def get_username(self):
        return self._bank._admin_user  

    def get_password(self):
        return self._bank._admin_pass 
    
    def get_bank_name(self):
        return self._bank._name  
    
    def get_same_bank_charges(self):
        return self._bank._same_bank_charges

    def get_other_bank_charges(self):
        return self._bank._other_bank_charges
