class AccountGetters:

    def __init__(self, account):
        self._account = account

    def get_account_id(self):
        return self._account._account_id

    def get_name(self):
        return self._account._name

    def get_balance(self):
        return self._account._balance

    def get_transactions_string(self):
        # Ensure _transactions is a valid list
        if not isinstance(self._account._transactions, list):
            return ["No transactions found."]
        return [str(txn) for txn in self._account._transactions] if self._account._transactions else ["No transactions found."]

    
    def get_transactions(self):
        # Return the actual Transaction objects
        return self._account._transactions if isinstance(self._account._transactions, list) else []

    def verify_password(self, password):
        return self._account._password == password
    

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
    

class TransactionGetters:
    def __init__(self, transaction):
        self._transaction = transaction

    def get_txn_id(self):
        return self._transaction._txn_id

    def get_account_id(self):
        return self._transaction._account_id

    def get_txn_type(self):
        return self._transaction._txn_type

    def get_amount(self):
        return self._transaction._amount

    def get_details(self):
        return self._transaction._details

    def get_timestamp(self):
        return self._transaction._timestamp
