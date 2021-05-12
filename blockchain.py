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
    blockTransaction = None

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
        
    def proofOfWork(self):
        initialTime = datetime.now()
        while self.blockHash[:self.hashDifficulty] != "0" * self.hashDifficulty:
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
       
    def createGenesisBlock(self):
        randomKey = ''.join(random.choice(string.ascii_lowercase) for i in range(30))
        return block(sha256(randomKey.encode('utf-8')).hexdigest(), self.hashDifficulty, transaction("0000", "0000", 0))   
    def getCurrentBlock(self):
        return self.blockchain[len(self.blockchain) - 1]

    def newBlock(self, transaction):
        self.blockchain.append(block(self.getCurrentBlock().blockHash, self.hashDifficulty, transaction))

    def validateBlockChain(self):
        for i in range(len(self.blockchain) - 1):
            if self.blockchain[i].blockHash !=  self.blockchain[i + 1].previousBlockHash :
                return False
        return True

    def addTransaction(self, newTransaction):
        if newTransaction.coins <= 0:
            return False
        self.transactions.append(newTransaction)
        return True

    def handleTransaction(self, miningRewardAddress):
        work = 0
        for i in range(len(self.transactions)):
            self.newBlock(self.transactions[i])
            work += 1

        self.transactions = []
        self.transactions.append(transaction("000", miningRewardAddress, self.miningReward * work))
    # This function gets the balance of specified address with checking all transactions within the blockchain.
    def getBalance(self, addressofBalance):
        availableCoins = 0
        for i in range(len(self.blockchain)):
            if self.blockchain[i].blockTransaction.destination == addressofBalance:
                availableCoins += self.blockchain[i].blockTransaction.coins
            elif self.blockchain[i].blockTransaction.source == addressofBalance:   
                availableCoins -= self.blockchain[i].blockTransaction.coins

        print(f"{addressofBalance}, available coins: {availableCoins}")        


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


block1 = blockchain(3,10) # Mining Difficulty and reward

block1.addTransaction(transaction("person1", "person2", 50))

block1.handleTransaction("person1") # Mining reward + 10
block1.handleTransaction("person1") # Mining reward + 10
block1.getBalance("person1") # person1, available coins: -40
block1.getBalance("person2") # person2, available coins: 50
