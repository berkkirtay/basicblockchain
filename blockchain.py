# This is my first blockchain implementation. 
# There can be many bugs or wrong approaches,
# please check the potential bugs before using!

from hashlib import sha256
import numpy as np
from datetime import datetime
import random
import string
import matplotlib.pyplot as plt

class block():
    previousBlockHash = ''
    blockHash = ''
    blockMineSize = 0
    hashDifficulty = 0
    validationTime = None
    blockTransaction = []
    # Each block has its unique hash string which is being generated with all essential informations in the block.
    def __init__(self, previousBlockHash, hashDifficulty, blockTransaction):
        self.hashDifficulty = hashDifficulty
        self.previousBlockHash = previousBlockHash
        self.blockTransaction = blockTransaction
        self.validationTime = datetime.now().strftime("%H:%M:%S")
        self.blockHash = self.generateBlockHash() 
        self.proofOfWork()

    def generateBlockHash(self):
        newhash = self.previousBlockHash + self.validationTime + str(self.blockTransaction) + str(self.blockMineSize)
        return sha256(newhash.encode('utf-8')).hexdigest()

    # This is the mining section. It generates hashes according to the difficulty and guarantees the security of the blockchain with the work done.  
    def proofOfWork(self):
        initialTime = datetime.now()
        while self.blockHash[len(self.blockHash) - self.hashDifficulty:] != "0" * self.hashDifficulty:
            self.blockHash = self.generateBlockHash()
            self.blockMineSize += 1

        finalTime = datetime.now() - initialTime
        print(f"Block hash = {self.blockHash}\nBlock is mined in {finalTime.total_seconds()} seconds.\n") 


class blockchain():
    blockchain = []
    hashDifficulty = 0
    miningReward = 0
    transactions = []
    def __init__(self, hashDifficulty, miningReward):
        print(f"Mining difficulty is {hashDifficulty}\n")
        self.hashDifficulty = hashDifficulty
        self.miningReward = miningReward
        self.blockchain = [self.createGenesisBlock()]
       # self.transactions 
    # Genesis block is the first node of the blockchain, so, we generated a random string for the starting point(hash).
    def createGenesisBlock(self):
        randomKey = ''.join(random.choice(string.ascii_lowercase) for i in range(30))
        genericTransactions = [transaction("null", "null", 0)]
        self.transactions = genericTransactions # First transaction of the blockchain.
        return block(sha256(randomKey.encode('utf-8')).hexdigest(), self.hashDifficulty, genericTransactions)   
    def getCurrentBlock(self):
        return self.blockchain[len(self.blockchain) - 1]

    def newBlock(self, transactions):
        self.blockchain.append(block(self.getCurrentBlock().blockHash, self.hashDifficulty, transactions))
        block1.validateBlockChain()

    def validateBlockChain(self):
        for i in range(len(self.blockchain) - 1):
            if self.blockchain[i].blockHash !=  self.blockchain[i + 1].previousBlockHash :
                print("Blockchain isn't valid!!!!.\n") 
                return False      
        return True

    def addTransaction(self, newTransaction):
        transactionCoins = self.getBalance(newTransaction.source, -1)
        if newTransaction.coins <= 0 or transactionCoins < newTransaction.coins:
            print(f"Insufficient coins in the source! {newTransaction.source} needs: {newTransaction.coins - transactionCoins}")
            return False

        self.transactions.append(newTransaction)
        return True

    def forceTransaction(self, newTransaction):
        print(f"Transaction is forced. {newTransaction.coins} added to {newTransaction.destination}")
        self.transactions.append(newTransaction)
        return True

    def handleTransaction(self, miningRewardAddress):
        if len(self.transactions) == 0:
            return False
        work = len(self.transactions)
        self.newBlock(self.transactions)  
        self.transactions = []
        self.transactions.append(transaction("null", miningRewardAddress, self.miningReward * work))
        return True

    # This function gets the balance of specified address with checking all transactions within the blockchain.
    def getBalance(self, addressofBalance, opt):
        availableCoins = 0
        for i in range(len(self.blockchain)):
            for j in range(len(self.blockchain[i].blockTransaction)):
                if self.blockchain[i].blockTransaction[j].destination == addressofBalance:
                    availableCoins += self.blockchain[i].blockTransaction[j].coins
                elif self.blockchain[i].blockTransaction[j].source == addressofBalance:   
                    availableCoins -= self.blockchain[i].blockTransaction[j].coins

        if opt == 0:
             print(f"{addressofBalance}, available coins: {availableCoins}") 
        return availableCoins 


class transaction():
    source = ''
    destination = ''
    coins = 0
    validationTime = None
    def __init__(self, source, destination, coins):
        self.source = source
        self.destination = destination
        self.coins = coins
        self.validationTime = datetime.now().strftime("%H:%M:%S")
    def generateTransactionHash(self):
        newHash = self.ssource + self.sdestination + str(self.scoins) + self.svalidationTime
        return sha256(newHash.encode('utf-8')).hexdigest()   


block1 = blockchain(4,0.2) # Mining Difficulty and reward
#block1.forceTransaction(transaction("null", "person1", 100))

# Mining section.
x = []
y = []
for i in range(50):
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
# Reward rate
plt.plot(x, y)
plt.xlabel("Mining reward")
plt.ylabel("Time")
plt.show()

