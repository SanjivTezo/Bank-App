import datetime
from models.transaction import Transaction
from models.bank import Bank  
import json, os

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
        if amount <= 0:
            return "Amount must be greater than zero."
        
        # ── SAME‑BANK existence check ───────────────────────────────────────────
        if same_bank and receiver_id not in self.bank.get_accounts():
            return "Receiver account not found in the same bank."
        # ── OTHER‑BANK existence check ──────────────────────────────────────────
        
        
        # ── If inter‑bank, load the other bank ───────────────────────────────────
        other_bank = None
        if not same_bank:
            

            other_bank_name = input("Enter receiver's Bank Name: ")
            filepath = "data/bank_data.json"
            if not os.path.exists(filepath):
                return "No banks data available."
            with open(filepath, "r") as f:
                all_banks = json.load(f)
            if other_bank_name not in all_banks:
                return f"Bank '{other_bank_name}' not found."
            ob = all_banks[other_bank_name]
            # construct and load the other Bank
            other_bank = Bank(ob["name"], ob["admin_user"], ob["admin_pass"])
            if receiver_id not in other_bank.get_accounts():
                return "Receiver account not found in that bank."

        # ── Confirm ───────────────────────────────────────────────────────────────
        confirm = input(f"Are you sure you want to transfer {amount} INR "
                        f"from {sender_id} to {receiver_id}? (yes/no): ").lower()
        if confirm != "yes":
            return "Transfer cancelled."

        # ── Compute charges & balances ───────────────────────────────────────────
        charge_pct = (self.bank._same_bank_charges if same_bank
                    else self.bank._other_bank_charges)["RTGS"]
        total_debit = amount + (amount * charge_pct / 100)
        sender_acct = self.bank.get_accounts()[sender_id]

        if sender_acct.get_balance() < total_debit:
            return "Insufficient balance!"

        # ── Perform debit on sender ─────────────────────────────────────────────
        sender_acct._balance -= total_debit
        txn_id_out = f"TXN{self.bank.get_bank_id()}{sender_id}" \
                    f"{datetime.datetime.now():%Y%m%d%H%M%S}"
        sender_acct._transactions.append(
            Transaction(txn_id_out, sender_id, "Transfer Out",
                        amount, receiver_id=receiver_id)
        )
        self.bank.save_to_json()

        # ── Perform credit on receiver ──────────────────────────────────────────
        if same_bank:
            recv_acct = self.bank.get_accounts()[receiver_id]
        else:
            recv_acct = other_bank.get_accounts()[receiver_id]

        recv_acct._balance += amount
        txn_id_in = f"TXN{(same_bank and self.bank or other_bank).get_bank_id()}" \
                    f"{receiver_id}{datetime.datetime.now():%Y%m%d%H%M%S}"
        recv_acct._transactions.append(
            Transaction(txn_id_in, receiver_id,
                        "Transfer In", amount, sender_id=sender_id)
        )

        # ── Save the other bank if needed ───────────────────────────────────────
        if not same_bank:
            other_bank.save_to_json()
        else:
            # already saved above, but you can call again if you like
            self.bank.save_to_json()

        return (f"{amount} INR transferred from {sender_id} to {receiver_id} "
                f"(charges: {charge_pct}%)")

    def view_all_transactions(self):
        transactions = []
        for account in self.bank.get_accounts().values():
            transactions.extend(account.get_transactions())
        return "\n".join(str(txn) for txn in transactions) if transactions else "No transactions found."
        
    def revert_transaction(self, account_id, txn_id):
        account = self.bank.get_accounts().get(account_id)
        if not account:
            return "Account not found."

        transaction_to_revert = None
        for txn in account.get_transactions():
            if txn.get_txn_id() == txn_id:
                transaction_to_revert = txn
                break

        if not transaction_to_revert:
            return "Transaction not found."

        txn_type = transaction_to_revert.get_txn_type()
        amount = transaction_to_revert.get_amount()
        details = transaction_to_revert.get_details()

        if txn_type == "Deposit":
            if account.get_balance() < amount:
                return "Insufficient balance to revert deposit."
            account._balance -= amount
            account._transactions.remove(transaction_to_revert)

        elif txn_type == "Withdraw":
            account._balance += amount
            account._transactions.remove(transaction_to_revert)

        elif txn_type == "Transfer Out":
            receiver_id = details["receiver_id"]
            receiver_account = self.bank.get_accounts().get(receiver_id)

            if not receiver_account:
                with open("data/bank_data.json", "r") as f:
                    all_banks = json.load(f)

                receiver_bank_data = None
                for bank_name, bank_info in all_banks.items():
                    if receiver_id in bank_info["accounts"]:
                        receiver_bank_data = bank_info
                        break

                if not receiver_bank_data:
                    return "Receiver's bank data not found."

                receiver_bank = Bank(receiver_bank_data["name"], receiver_bank_data["admin_user"], receiver_bank_data["admin_pass"])
                receiver_account = receiver_bank.get_accounts().get(receiver_id)

                if not receiver_account:
                    return "Receiver account not found in their bank."

                if receiver_account.get_balance() < amount:
                    return "Receiver has insufficient funds to revert transfer."

                account._balance += amount
                receiver_account._balance -= amount

                for txn in receiver_account.get_transactions():
                    if txn.get_txn_type() == "Transfer In" and txn.get_details().get("sender_id") == account_id and txn.get_amount() == amount:
                        receiver_account._transactions.remove(txn)
                        break

                account._transactions.remove(transaction_to_revert)
                self.bank.save_to_json()
                receiver_bank.save_to_json()
                return f"Transaction {txn_id} reverted successfully!"

            else:
                if receiver_account.get_balance() < amount:
                    return "Receiver has insufficient funds to revert transfer."

                account._balance += amount
                receiver_account._balance -= amount

                for txn in receiver_account.get_transactions():
                    if txn.get_txn_type() == "Transfer In" and txn.get_details().get("sender_id") == account_id and txn.get_amount() == amount:
                        receiver_account._transactions.remove(txn)
                        break

                account._transactions.remove(transaction_to_revert)

        elif txn_type == "Transfer In":
            sender_id = details["sender_id"]
            sender_account = self.bank.get_accounts().get(sender_id)

            if not sender_account:
                with open("data/bank_data.json", "r") as f:
                    all_banks = json.load(f)

                sender_bank_data = None
                for bank_name, bank_info in all_banks.items():
                    if sender_id in bank_info["accounts"]:
                        sender_bank_data = bank_info
                        break

                if not sender_bank_data:
                    return "Sender's bank data not found."

                sender_bank = Bank(sender_bank_data["name"], sender_bank_data["admin_user"], sender_bank_data["admin_pass"])
                sender_account = sender_bank.get_accounts().get(sender_id)

                if not sender_account:
                    return "Sender account not found in their bank."

                if account.get_balance() < amount:
                    return "Insufficient balance to revert transfer."

                account._balance -= amount
                sender_account._balance += amount

                for txn in sender_account.get_transactions():
                    if txn.get_txn_type() == "Transfer Out" and txn.get_details().get("receiver_id") == account_id and txn.get_amount() == amount:
                        sender_account._transactions.remove(txn)
                        break

                account._transactions.remove(transaction_to_revert)
                self.bank.save_to_json()
                sender_bank.save_to_json()
                return f"Transaction {txn_id} reverted successfully!"

            else:
                if account.get_balance() < amount:
                    return "Insufficient balance to revert transfer."

                account._balance -= amount
                sender_account._balance += amount

                for txn in sender_account.get_transactions():
                    if txn.get_txn_type() == "Transfer Out" and txn.get_details().get("receiver_id") == account_id and txn.get_amount() == amount:
                        sender_account._transactions.remove(txn)
                        break

                account._transactions.remove(transaction_to_revert)

        self.bank.save_to_json()
        return f"Transaction {txn_id} reverted successfully!"
