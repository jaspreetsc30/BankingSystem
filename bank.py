import re
import json
from datetime import datetime
from datetime import timedelta
from sqlite3 import Timestamp

BANK_ID = "A0000000"
BANK_USERNAME = "OSL_FEE"
VALID_CURRENCIES = ["USD" , "HKD" , "SGD"]
WITHDRAWAL_LIMIT = 5
WITHDRAWAL_BAN_TILL_RESET = 5

class Bank:
    accounts = {}
    transactions = {}
    def __init__(self,id: str) -> None:
        self.__id = id 
        infoFile = open('accounts.json', "r")
        txFile = open("transactions.json")
        
        try:
            Bank.accounts = json.load(infoFile)["accounts"]
            Bank.transactions = json.load(txFile)["transactions"]
        except json.JSONDecodeError:
            pass

        return
    
    

    def __addTransaction(self, date: str , currency: str , operation: str , amount: str, recipient: str = None)->None:
        quaduple = (date,currency,operation,amount)
        userId = self.__id if recipient == None else recipient
        
        if userId not in Bank.transactions.keys():
            Bank.transactions[userId] = [quaduple]
        else:
            Bank.transactions[userId].append(quaduple)
        return


    def createAccount(self , userName:str, currency:str)-> None :
        #must be valid id
        if not re.match(r"^[A-Z]{1}[0-9]{6}[a-zA-Z0-9]{1}", self.__id):
            print("Please provide a valid ID number")
            return

        if currency not in VALID_CURRENCIES:
            print("Please provide a valid currency[SGD,HKD,USD] or create an account for the specified currency}")
            return

        #check if account has been created before
        if self.__id not in Bank.accounts.keys():
            #add OSL account if does not exist
            if BANK_ID not in Bank.accounts.keys():
                Bank.accounts[BANK_ID] ={
                    "userName": "OSL_FEE" ,
                    "USD" : 0,
                    "HKD" : 0,
                    "SGD" : 0 
                }
            
            Bank.accounts[self.__id] ={
                "userName": userName ,
                currency : 0,
                "withdrawalBanPeriod" : datetime.now().replace(microsecond=0),
                "withdrawalCounter": 0, 
            }
            self.__saveChanges()
            print(f"Congratulations {userName} of id {self.__id}. Your account has been created. ")

        elif currency not in  Bank.accounts[self.__id].keys():
            Bank.accounts[self.__id][currency] = 0
            self.__saveChanges()
            print(f"Congratulations {userName} of id {self.__id}. Your account also supports {currency}. ")

        else:
            print(f"The Account has already been created with the given id {self.__id} and currency {currency}")

        return

    def deposit(self,currency:str ,amt: float)->None :
        #check that id is valid
        if self.__id not in Bank.accounts.keys():
            print(f"The account with the specified id {self.__id} does not exist")
            return
        #appropriate currency
        if currency not in VALID_CURRENCIES or currency not in Bank.accounts[self.__id].keys():
            print("Please provide a valid currency[SGD,HKD,USD] or create an account for the specified currency}")
            return

        Bank.accounts[self.__id][currency] += amt
        self.__addTransaction(datetime.now().replace(microsecond=0) , currency, "DEPOSIT",amt)
        self.__saveChanges()
        print(f"{amt} {currency} has been deposited")
        
        return       

    def transfer(self, currency: str ,  amt: float ,recipient:str):
        if self.__id not in Bank.accounts.keys() or currency not in Bank.accounts[self.__id].keys():
            print(f"The sender account with the specified id {self.__id} does not exist")
            return
        if recipient not in Bank.accounts.keys() or currency not in Bank.accounts[recipient].keys():
            print(f"The recipient account with the specified id {self.__id} does not exist or the account holder does not have an account in {currency} currency")
            return

        if (Bank.accounts[self.__id][currency] > amt *1.01):
            fee = amt*0.01
            Bank.accounts[self.__id][currency] -=(amt + fee)
            Bank.accounts[recipient][currency] += amt
            Bank.accounts[BANK_ID][currency] += fee
            currTime = datetime.now().replace(microsecond=0)
            self.__addTransaction(currTime,currency,f"TRANSFER to {recipient}",-amt)
            self.__addTransaction(currTime,currency,f"TRANSFER FEE  ",-fee)
            self.__addTransaction(currTime,currency,f"TRANSFER FROM {self.__id}",amt, recipient)
            self.__addTransaction(currTime,currency,f"TRANSFER FEE FROM {self.__id}",fee, BANK_ID)
            self.__saveChanges()
            print(f"{amt} {currency} has been transferred from your account to id holder {recipient}")
        else:
            print("Not enough balance to transfer money")

        return
    
    def withdraw(self,  currency: str , amt: float ):
        if self.__id not in Bank.accounts.keys() or currency not in Bank.accounts[self.__id].keys():
            print(f"The account with the specified id {self.__id} does not exist or does not have a {currency} account")
            return

        currentTime = datetime.now().replace(microsecond=0)
        bannedTime = datetime.strptime(Bank.accounts[self.__id]["withdrawalBanPeriod"], '%Y-%m-%d %H:%M:%S')
        if currentTime < bannedTime:
            timeLeft = ( bannedTime - currentTime)
            print(f"You have already done 5 withdrawals within 5 minutes, please wait for {timeLeft}")
            return

        if Bank.accounts[self.__id][currency] > 1.01* amt:
            fee = amt*0.01
            Bank.accounts[self.__id][currency] -=(amt+fee)
            Bank.accounts[BANK_ID][currency] += fee
            Bank.accounts[self.__id]["withdrawalCounter"] += 1
            if Bank.accounts[self.__id]["withdrawalCounter"] %WITHDRAWAL_LIMIT == 0 :
                Bank.accounts[self.__id]["withdrawalBanPeriod"] = datetime.now().replace(microsecond=0) + timedelta(minutes=WITHDRAWAL_BAN_TILL_RESET)
                Bank.accounts[self.__id]["withdrawalCounter"] = 0 
            
            currTime = datetime.now().replace(microsecond=0)
            self.__addTransaction(currTime,currency,"WITHDRAWAL",-amt)
            self.__addTransaction(currTime,currency,f"WITHDRAWAL FEE  ",-fee)
            self.__addTransaction(currTime,currency,f"WITHDRAWAL FEE FROM {self.__id}",fee, BANK_ID)
            self.__saveChanges()
            print(f"{amt} {currency} has been withdrawn from your account")

        else:
            print("Not enough money to withdraw")

        return

    def balance(self,):
        if self.__id not in Bank.accounts.keys() :
            print(f"The sender account with the specified id {self.__id} does not exist")
            return
        
        print("Your balance is as follows:")
        for currency in VALID_CURRENCIES:
            if currency in Bank.accounts[self.__id].keys():
                print(f"{currency}: {Bank.accounts[self.__id][currency]}")    

        return
    
    
    
    def printStatement(self):
        userName = Bank.accounts[self.__id]["userName"]
        print(f"User Name:\n{userName}")
        txList = Bank.transactions[self.__id]

        print( '{:<20s} {:<10s} {:<30s}  {:<15s}'.format("Date", "Currency", "Operation", "Amount") )

        for tx in txList:
            print( '{:<20s} {:<10s} {:<30s}  {:<15f}'.format(tx[0],tx[1],tx[2],tx[3]) )
        
        return


    def __saveChanges(self):
        accounts = {"accounts" : Bank.accounts}
        transactions = {"transactions" : Bank.transactions}

        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, default=str)

        with open('transactions.json', 'w') as f:
            json.dump(transactions, f, default=str)
        
