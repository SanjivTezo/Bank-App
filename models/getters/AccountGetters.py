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
        if not isinstance(self._account._transactions, list):
            return ["No transactions found."]
        return [str(txn) for txn in self._account._transactions] if self._account._transactions else ["No transactions found."]

    
    def get_transactions(self):
        return self._account._transactions if isinstance(self._account._transactions, list) else []

    def verify_password(self, password):
        return self._account._password == password
    
