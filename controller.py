import json
from bank import Bank 
import sys


MAX_ARGUMENTS = 6
MIN_ARGUMENTS = 3

VALID_REQUESTS = ["create" , "deposit" , "withdraw" , "transfer" , "balance" , "statement" ]


if __name__ == "__main__":
    argsLen = len(sys.argv)
    request = sys.argv[1] if argsLen >= 2 else 0 
    if MIN_ARGUMENTS > argsLen or  argsLen > MAX_ARGUMENTS:
        print("Invalid number of parameters")
    elif sys.argv[1] not in VALID_REQUESTS:
        print("Please specify a valid request")
    else:
        user = Bank(sys.argv[2])
        if request == "create" and argsLen == 5:
            user.createAccount(sys.argv[3],sys.argv[4])
        elif request == "deposit" and argsLen == 5:
            user.deposit(sys.argv[3],float(sys.argv[4]))
        elif request == "withdraw" and argsLen == 5:
            user.withdraw(sys.argv[3],float(sys.argv[4]))
        elif request == "transfer" and argsLen == 6:
            user.transfer(sys.argv[3],float(sys.argv[4]),sys.argv[5])
        elif request == "balance" and argsLen == 3:
            user.balance()
        elif request == "statement" and argsLen == 3:
            user.printStatement()
        else :
            print(f"Invalid number of parameters for request {request}")

        


    