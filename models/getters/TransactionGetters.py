
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
