import datetime

class Transaction:
    def __init__(self, txn_id, account_id, txn_type, amount, **kwargs):
        self._txn_id = txn_id  
        self._account_id = account_id  
        self._txn_type = txn_type  
        self._amount = amount  
        self._details = kwargs  
        self._timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    def __str__(self):
        return f"Transaction[ID: {self._txn_id}, Type: {self._txn_type}, Amount: {self._amount}, Details: {self._details}, Timestamp: {self._timestamp}]"

    def to_dict(self):
        return {
            "txn_id": self._txn_id,
            "account_id": self._account_id,
            "txn_type": self._txn_type,
            "amount": self._amount,
            "details": self._details,
            "timestamp": self._timestamp
        }

    def get_txn_id(self):
        return self._txn_id

    def get_account_id(self):
        return self._account_id

    def get_txn_type(self):
        return self._txn_type

    def get_amount(self):
        return self._amount

    def get_details(self):
        return self._details

    def get_timestamp(self):
        return self._timestamp