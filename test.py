import numpy as np
from datetime import datetime
import random
import string
import matplotlib.pyplot as plt
from hashlib import sha256

from blockchain import *

block1 = blockchain(2,0.2) # Mining Difficulty and reward
#block1.forceTransaction(transaction("null", "person1", 100))

# Mining section.
x = []
y = []
for i in range(10):
    initialTime = datetime.now()
    block1.handleTransaction("person1") # Mining reward + 0.2
    finalTime = datetime.now() - initialTime
    x.append(block1.getBalance("person1", 0))
    y.append(finalTime.total_seconds())
    if len(x) > 2:
        x[len(x) - 1] += x[len(x) - 2]
        y[len(x) - 1] += y[len(x) - 2]

block1.addTransaction(transaction("person1", "person2", 10))
block1.handleTransaction("person1") # Mining reward + 0.2
block1.getBalance("person1", 0) # person1, available coins
block1.getBalance("person2", 0) # person2, available coins

wallet1 = wallet("person1", "null")
wallet1.updateTransactions(block1)

# Reward rate
plt.plot(x, y)
plt.xlabel("Mining reward")
plt.ylabel("Time")
plt.show()

