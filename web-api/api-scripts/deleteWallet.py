from blockchain import * 
from save import *
import sys


block1 = loadBlock()
wallets = loadWallets()

newpublicName = sys.argv[1]

for i in range(len(wallets) - 1):
    if wallets[i].publicAddress == newpublicName:
        wallets.pop(i)
        break
        
save(block1, wallets)


