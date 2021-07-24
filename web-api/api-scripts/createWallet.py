from blockchain import * 
from save import *
import sys


block1 = loadBlock()
wallets = loadWallets()

newpublicName = sys.argv[1]
newWallet = wallet(newpublicName, newpublicName) 
newWallet.updateTransactions(block1)
wallets.append(newWallet)

save(block1, wallets)

print("Wallet creation is successful.")