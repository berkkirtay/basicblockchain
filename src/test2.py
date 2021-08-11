from datetime import datetime
import random
import string

from hashlib import sha256

from blockchain import *


block1 = blockchain(2, 0.2)  # Mining Difficulty and reward
#block1.forceTransaction(transaction("null", "person1", 100))
# Mining section.

block1.forceTransaction(transaction("null", "person1", 10000))

block1.addTransaction(transaction("person1", "person2", 10))
block1.handleTransaction("person1")  # Mining reward + 0.2
block1.getBalance("person1")  # person1, available coins
block1.getBalance("person2")  # person2, available coins

wallet1 = wallet("person1", "person1")
wallet1.updateTransactions(block1)

wallet2 = wallet("person2", "person2")
wallet2.updateTransactions(block1)

wallets = [wallet1, wallet2]
