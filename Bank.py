import datetime
import random
class Bank:
    def __init__(self, name):
        self.name=name
        self.bank_id=name[:3].upper()+ datetime.datetime.now().strftime("%Y%m%d")
        self.rtgs_charges={"same_bank":0,"other_bank":2}
        self.imps_charges={"same_bank":5,"other_bank":6}    
        self.accepted_currencies={"INR":1}
        self.accounts={}
        self.transactions=[]

    def display_bank_details(self):
        print(f"\nBank Name: {self.name} (ID: {self.bank_id})")
        print("RTGS Charges:",self.rtgs_charges)
        print("Imps Charges:",self.imps_charges)
        print("Accepted Currencies:",self.accepted_currencies)

    def create_account(self,name):
        account_id=name[:3].upper()+datetime.datetime.now().strftime("%Y%m%d")
        password=str(random.randint(1000,9999)) 
        self.accounts[account_id]={"name":name,"password":password,"balance":0}
        print(f"Account created! ID:{account_id},password:{password}")
    
    def update_account(self,account_id,new_name):
        if account_id in self.accounts:
            old_name=self.accounts[account_id]["name"]
            self.accounts[account_id]["name"]=new_name
            print(f"Account {account_id} updated  form {old_name} to {new_name} successfully!")
        else:   
            print("Account not found.")

    def delete_account(self,account_id):
        if(account_id in self.accounts):
            del self.accounts[account_id]
            print("Account deleted successfully!")
        else:
            print("Account not found.")
            
    def add_currency(self,currency,exchange_rate):
        self.accepted_currencies[currency]=exchange_rate
        print(f"{currency} added with exchange rate {exchange_rate}")

    def set_rtgs_charge(self,same_bank,other_bank):
        self.rtgs_charges={"same_bank":same_bank,"other_bank":other_bank}
        print("RTGS charges updated.")

    def set_imps_charge(self,same_bank,other_bank):
        self.imps_charges={"same_bank":same_bank,"other_bank":other_bank}
        print("IMPS charges updated.")

    def view_transactions(self,account_id=None):
        print("\nTransaction History:")
        for txn in self.transactions:
            if account_id is None or txn["account_id"]==account_id:
                print(txn)

    def revert_transaction(self,txn_id):
        for txn  in self.transactions:
            if txn["id"] == txn_id:
                self.transactions.remove(txn)
                print("Transaction reverted successfully!")
                return
        print("Transaction not found.")
    
    def all_account_details(self):
        if not self.accounts:
            print("No accounts found!")
            return
        print("\nAll Account Details:")
        for account_id, account_info in self.accounts.items():
            print(f"Account ID: {account_id}, Name: {account_info['name']}, Balance: {account_info['balance']}")
    
    def display_currency_details(self):
        if not self.accepted_currencies:
            print("\nNo currencies available.")
            return
        print("\nAll Currency Details:")
        for currency, exchange_rate in self.accepted_currencies.items():
            print(f"{currency}: {exchange_rate}")
    
    def display_transaction_charges(self):
        print(f"RTGS Charges: {self.rtgs_charges}")
        print(f"IMPS Charges: {self.imps_charges}")





    def deposit(self,account_id,amount,currency):
        if account_id in self.accounts:
            if currency in self.accepted_currencies:
                converted_amount=amount*self.accepted_currencies[currency]
                self.accounts[account_id]["balance"]+=converted_amount
                txn_id=f"TXN{self.bank_id}{account_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.transactions.append({"id":txn_id,"account_id":account_id,type:"Deposit","amount":converted_amount})
                print (f"Deposited {converted_amount} INR to  {account_id} successfully!")
            else:
                print("Currency not accepted.")
        else:
            print("Account not found.")

    def withdraw(self,account_id,amount):
        if account_id in self.accounts:
            if self.accounts[account_id]["balance"] >=amount:
                self.accounts[account_id]["balance"]-=amount
                txn_id=f"TXN{self.bank_id}{account_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.transactions.append({"id":txn_id,"account_id":account_id,type:"Withdraw","amount":amount})
                print(f"Withdrawn {amount} INR from {account_id} successfully!")
            else:
                print("Insufficient balance!")
        else:
            print("Account not found.")

    def transfer(self ,sender_id,receiver_id,amount, same_bank=True):
        if sender_id in self.accounts and receiver_id in self.accounts:
                charge=self.rtgs_charges["same_bank"] if same_bank else self.rtgs_charges["other_bank"]
                total_deduction=amount+(amount*charge/100)

                if self.accounts[sender_id]["balance"]>=total_deduction:
                    self.accounts[sender_id]["balance"]-=total_deduction
                    self.accounts[receiver_id]["balance"]+=amount

                    txn_id_sender=f"TXN{self.bank_id}{sender_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    txn_id_receiver = f"TXN{self.bank_id}{receiver_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

                    self.transactions.append({"id":txn_id_sender,"account_id":sender_id,"type":"Transfer","amount":amount, "to":receiver_id})
                    self.transactions.append({"id": txn_id_receiver, "account_id": receiver_id, "type": "Transfer Received", "amount": amount, "from": sender_id})

                    print(f"{amount} INR transferred from {sender_id} to {receiver_id} (charges:{charge}%)")
                else:
                    print("Insufficient balance!")
        else:
            print("Invalid account details.")
           

def main():
    bank=Bank("SBI")
    # bank.display_bank_details()
    while True:
        print("\n1.Login as Bank Staff:")
        print("2.Login as Account Holder:")
        print("3.Exit")

        choice=input("Enter your choice:")
        if choice=="1":
            password=input("Enter yout staff password:")
            if password=="a":
                while True: 
                    print("\nBank Staff Menu:")
                    print("1. Create Account")
                    print("2. Update Account")
                    print("3. Delete Account")
                    print("4. Add Currency")
                    print("5. Set RTGS Charges")
                    print("6. Set IMPS Charges")
                    print("7. View Transactions")
                    print("8. Revert Transaction")
                    print("9. All Account Details")
                    print("10. See All Currency Details")
                    print("11. See Transaction Charges")

                    print("12. Logout")

                    option = input("Enter option: ")

                    if option=="1":
                        name=input("Enter Account Holder Name:")
                        bank.create_account(name)


                    elif option=="2":
                        account_id=input("Enter Account ID:")
                        new_name=input("Enter New Name:")
                        bank.update_account(account_id,new_name)

                    elif option=="3":
                        account_id=input("Enter Account ID:")
                        bank.delete_account(account_id)

                    elif option=="4":
                        currency=input("Enter Currency:")
                        exchange_rate=float(input("Enter Exchange Rate:"))
                        bank.add_currency(currency,exchange_rate)

                    elif option=="5":
                        same=float(input("Enter Same Bank RTGS Charg(%): "))
                        other=float(input("Enter Other Bank RTGS Charge(%): "))
                        bank.set_rtgs_charge(same,other)

                    elif option=="6":
                        same=float(input("Enter Same Bank IMPS Charge(%): "))
                        other=float(input("Enter Other Bank IMPS Charge(%): "))
                        bank.set_imps_charge(same,other)

                    elif option=="7":
                        bank.view_transactions()

                    elif option=="8":
                        txn_id=input("Enter Transaction ID:")
                        bank.revert_transaction(txn_id)
                    elif option=="9":
                        bank.all_account_details()
                    
                    elif option=="10":
                        bank.display_currency_details()
                    
                    elif option=="11":
                        bank.display_transaction_charges()

                    elif option=="12":
                        break

        elif choice=="2":
            account_id=input("Enter Account ID:")
            password=input("Enter Password:")
            if account_id in bank.accounts and bank.accounts[account_id]["password"]==password:

                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer Funds")
                    print("4. View Transactions")
                    print("5. Check Balnce")
                    print("6. Logout") 

                    options=input("Enter your choice:")   
                    if options=="1":
                        amount=float(input("Enter amount:"))
                        currency=input("Enter currency:")
                        bank.deposit(account_id,amount,currency)

                    elif options=="2":
                        amount = float(input("Enter amount: "))
                        bank.withdraw(account_id, amount)

                    elif options=="3":
                        receiver_id=input("Enter receiver account ID:")
                        amount = float(input("Enter amount: "))
                        bank.transfer(account_id,receiver_id,amount)

                    elif options=="4":
                        bank.view_transactions(account_id)

                    elif options=="5":  
                        print(f"Balance: {bank.accounts[account_id]['balance']} INR")

                    elif options=="6":  
                        break
                    
        elif choice=="3":
            break                     

if __name__ == "__main__":
    main()
