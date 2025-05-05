import datetime

class Transaction:
    def __init__(self, txn_id, account_id, txn_type, amount, **details):
        self._txn_id = txn_id
        self._account_id = account_id
        self._txn_type = txn_type
        self._amount = amount
        self._details = details
        self._timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "transaction_id": self._txn_id,
            "account_id": self._account_id,
            "txn_type": self._txn_type,
            "amount": self._amount,
            "details": self._details,
            "timestamp": self._timestamp
        }

