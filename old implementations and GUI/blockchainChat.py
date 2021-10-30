import numpy as np
from datetime import datetime
import random
import string
import matplotlib.pyplot as plt
from hashlib import sha256

from blockchain import *


class blockchainChat(blockchain):
    # We take advantage of the normal blockchain class implementation.
    # Transactions are overridden by textTransactions and same thing goes for coins(texts) as well.
    texts = []

    def __init__(self, hashDifficulty, miningReward):
        super().__init__(hashDifficulty, miningReward)
        self.transactions = []

    def createGenesisBlock(self):
        randomKey = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(30))
        genericTransactions = [textTransactions("Chat", "null", "Genesis")]
        # First transaction of the blockchain.
        self.transactions = genericTransactions
        return block(sha256(randomKey.encode('utf-8')).hexdigest(), self.hashDifficulty, genericTransactions)

    def addText(self, newText):
        self.transactions.append(newText)
        return True

    # Transactions as texts
    def handleChat(self):
        if len(self.transactions) == 0:
            return False
        work = len(self.transactions)
        self.newBlock(self.transactions)
        self.transactions = []
        # We need a different approach here for proof of work.
        #self.transactions.append(transaction("null", miningRewardAddress, self.miningReward * work))
        return True

    def getText(self):
        for i in range(len(self.blockchain)):
            for j in range(len(self.blockchain[i].blockTransactions)):
                self.texts.append(
                    f'{self.blockchain[i].blockTransactions[j].source}: {self.blockchain[i].blockTransactions[j].coins}')


class textTransactions(transaction):
    def __init__(self, source, destination, texts):
        super().__init__(source, destination, texts)


newchat = blockchainChat(2, 0)
# p2p approach
newchat.addText(textTransactions("berk", "someone", "hey!"))
newchat.addText(textTransactions("someone", "berk", "hey berk!"))

newchat.handleChat()
newchat.getText()
for text in newchat.texts:
    print(text)
