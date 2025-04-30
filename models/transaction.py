import datetime

class Transaction:
    def __init__(self, txn_id, account_id, txn_type, amount, **details):
        self._txn_id = txn_id
        self._account_id = account_id
        self._txn_type = txn_type
        self._amount = amount
        self._details = details
        self._timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        details_str = ", ".join(f"{key}: {value}" for key, value in self._details.items())
        return f"Transaction[ID: {self._txn_id}, Type: {self._txn_type}, Amount: {self._amount}, Details: {{{details_str}}}]"

    def to_dict(self):
        return {
            "txn_id": self._txn_id,
            "account_id": self._account_id,
            "txn_type": self._txn_type,
            "amount": self._amount,
            "details": self._details,
            "timestamp": self._timestamp
        }

