from blockchain import * 
from datetime import datetime
from save import *

block1 = loadBlock()
wallets = loadWallets()

save(block1, wallets)


