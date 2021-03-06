import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

from blockchain import *


block1 = blockchain(2, 0.2)  # Mining Difficulty and reward

# Mining section.
x = []
y = []
for i in range(500):
    initialTime = datetime.now()
    block1.handleTransaction("person1")  # Mining reward + 0.2
    finalTime = datetime.now() - initialTime
    x.append(block1.getBalance("person1"))
    y.append(finalTime.total_seconds())
    if len(x) > 2:
        x[len(x) - 1] += x[len(x) - 2]
        y[len(x) - 1] += y[len(x) - 2]

block1.addTransaction(transaction("person1", "person2", 10))
block1.handleTransaction("person1")  # Mining reward + 0.2
block1.getBalance("person1")  # person1, available coins
block1.getBalance("person2")  # person2, available coins

wallet1 = wallet("person1", "person1")
wallet1.updateTransactions(block1)

wallet2 = wallet("person2", "person2")
wallet2.updateTransactions(block1)

wallets = [wallet1, wallet2]

database1 = database()
database1.saveDatabase(block1, wallets, '')
database1.loadDatabase('')


# Reward rate
plt.plot(y, x)
plt.xlabel("Time")
plt.ylabel("Mining reward")
plt.show()
