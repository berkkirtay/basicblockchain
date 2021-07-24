from blockchain import * 
from save import *
import sys

block1 = loadBlock()
wallets = loadWallets()

sourceAddress = sys.argv[1]
destAddress = sys.argv[2]
transactionAmount = int(sys.argv[3])

# We are assuming "berk" is the admin of this blockchain and can make transactions forcefully.
# This option is only for tests.

if sourceAddress == "berk":
    block1.forceTransaction(transaction("null", sourceAddress, transactionAmount))
    block1.handleTransaction("null")
else:    
    block1.addTransaction(transaction(sourceAddress, destAddress, transactionAmount))
    block1.handleTransaction("null")

save(block1, wallets)