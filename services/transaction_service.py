import datetime
from transaction import Transaction  

class TransactionService:
    def __init__(self, bank):
        self.bank = bank

    def deposit(self, account_id, amount, currency):
        if account_id not in self.bank.get_accounts():
            return "Account not found."
        if currency not in self.bank.get_accepted_currencies():
            return f"Currency {currency} not accepted."
        if amount <= 0:
            return "Amount must be greater than zero."
        result = self.bank.get_accounts()[account_id].deposit(amount, currency, self.bank.get_accepted_currencies()[currency])
        self.bank.save_to_json()
        return result

    def withdraw(self, account_id, amount):
        if account_id not in self.bank.get_accounts():
            return "Account not found."
        if amount <= 0:
            return "Amount must be greater than zero."
        result = self.bank.get_accounts()[account_id].withdraw(amount)
        self.bank.save_to_json()
        return result

    def transfer(self, sender_id, receiver_id, amount, same_bank=True):
        if sender_id not in self.bank.get_accounts():
            return "Sender account not found."
        if receiver_id not in self.bank.get_accounts():
            return "Receiver account not found."
        if amount <= 0:
            return "Amount must be greater than zero."

        confirm = input(f"Are you sure you want to transfer {amount} INR from {sender_id} to {receiver_id}? (yes/no): ").lower()
        if confirm != "yes":
            return "Transfer cancelled."

        charge = self.bank._same_bank_charges["RTGS"] if same_bank else self.bank._other_bank_charges["RTGS"]
        total_deduction = amount + (amount * charge / 100)

        if self.bank.get_accounts()[sender_id].get_balance() >= total_deduction:
            self.bank.get_accounts()[sender_id]._balance -= total_deduction
            self.bank.get_accounts()[receiver_id]._balance += amount
            txn_id_sender = f"TXN{self.bank.get_bank_id()}{sender_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            txn_id_receiver = f"TXN{self.bank.get_bank_id()}{receiver_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.bank.get_accounts()[sender_id]._transactions.append(Transaction(txn_id_sender, sender_id, "Transfer Out", amount, receiver_id=receiver_id))
            self.bank.get_accounts()[receiver_id]._transactions.append(Transaction(txn_id_receiver, receiver_id, "Transfer In", amount, sender_id=sender_id))
            self.bank.save_to_json()
            return f"{amount} INR transferred from {sender_id} to {receiver_id} (charges: {charge}%)"
        return "Insufficient balance!"

    def view_all_transactions(self):
        transactions = []
        for account in self.bank.get_accounts().values():
            transactions.extend(account.get_transactions())
        return "\n".join(str(txn) for txn in transactions) if transactions else "No transactions found."

    def revert_transaction(self, account_id, txn_id):
        if account_id not in self.bank.get_accounts():
            return "Account not found."

        account = self.bank.get_accounts()[account_id]
        
        txn_to_revert = None
        for txn in account.get_transactions():
            if txn.get_txn_id() == txn_id:
                txn_to_revert = txn
                break
        
        if not txn_to_revert:
            return "Transaction not found."

        txn_type = txn_to_revert.get_txn_type()
        amount = txn_to_revert.get_amount()
        details = txn_to_revert.get_details()

        try:
            if txn_type == "Deposit":
                if account.get_balance() - amount < 0:
                    return "Error: Reverting would make account balance negative"
                account._balance -= amount

            elif txn_type == "Withdraw":
                account._balance += amount

            elif txn_type == "Transfer Out":
                receiver_id = details["receiver_id"]
                if receiver_id not in self.bank.get_accounts():
                    return "Receiver account not found"
                
                receiver = self.bank.get_accounts()[receiver_id]
                
                if account.get_balance() + amount < 0:
                    return "Error: Reverting would make sender balance negative"
                if receiver.get_balance() - amount < 0:
                    return "Error: Reverting would make receiver balance negative"
                
                account._balance += amount
                receiver._balance -= amount
                
                for txn in receiver.get_transactions():
                    if (txn.get_txn_type() == "Transfer In" and 
                        txn.get_details().get("sender_id") == account_id and
                        txn.get_amount() == amount):
                        receiver._transactions.remove(txn)
                        break

            elif txn_type == "Transfer In":
                sender_id = details["sender_id"]
                if sender_id not in self.bank.get_accounts():
                    return "Sender account not found"
                
                sender = self.bank.get_accounts()[sender_id]
                
                if account.get_balance() - amount < 0:
                    return "Error: Reverting would make receiver balance negative"
                if sender.get_balance() + amount < 0:
                    return "Error: Reverting would make sender balance negative"
                
                account._balance -= amount
                sender._balance += amount
                

                for txn in sender.get_transactions():
                    if (txn.get_txn_type() == "Transfer Out" and 
                        txn.get_details().get("receiver_id") == account_id and
                        txn.get_amount() == amount):
                        sender._transactions.remove(txn)
                        break

            account._transactions.remove(txn_to_revert)
            self.bank.save_to_json()
            return f"Transaction {txn_id} reverted successfully!"

        except Exception as e:
            return f"Error reverting transaction: {str(e)}"