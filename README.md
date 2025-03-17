It is console application that Simulate a bank account which supports creation of account, closing an account, withdrawals, deposits, transfer funds

Use cases to be taken into consideration while developing the application:
1.	Setup new Bank
        a.	Set Default RTGS and IMPS charges for same bank 
            i.	RTGS-0%
            ii.	IMPS-5%
        b.	Set Default RTGS and IMPS charges for other bank 
            i.	RTGS- 2%
            ii.	IMPS- 6%
        c.	Add default accepted currency as INR
2.	Create a page where user will get options to login as account holder or bank staff
3.	If User is bank staff then he should be able to perform following actions
        a.	Create new account and give username and password to account holder
        b.	Update / Delete account at any time
        c.	Add new Accepted currency with exchange rate 
        d.	Add service charge for same bank account
                i.	RTGS
                ii.	IMPS
        e.	Add service charge for other bank account
                i.	RTGS
                ii.	IMPS
        f.	Can view account transaction history
        g.	Can revert any transaction
4.	If User is account holder he should be able to perform following actions 
        a.	Deposit amount (any currency but bank will convert it to INR and will accept the deposit)
        b.	Withdraw amount (INR only)
        c.	Transfer funds (INR only)
        d.	Can view his transaction history
NOTE:
1.	Bank ID pattern - Starting 3 letters of bank name + current date
2.	Account ID pattern -  Starting 3 letters of account holder name + current date 
3.	Transaction ID Pattern – “TXN” + bank ID + Account ID + current date
 
