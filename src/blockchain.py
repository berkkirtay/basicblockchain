# This is my first blockchain implementation.
# There can be many bugs or wrong approaches,
# please check the potential bugs before using!
# Developed by Berk Kırtay

'''
MIT License

Copyright (c) 2021 Berk Kırtay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from hashlib import sha1, sha256
from datetime import datetime
import random
import string
import pickle
import rsa

(RSA_PublicKey, RSA_PrivateKey) = rsa.newkeys(512, 4)


# Every block keeps previous block's hash for validation of blockchain.
# We create a hash code based on previous block's hash,
# block's validation time and transactions.

class block():
    previousBlockHash = ''
    blockHash = ''
    blockMineSize = 0
    hashDifficulty = 0
    validationTime = None
    blockTransactionCapacity = 100
    blockTransactions = []
    # Each block has its unique hash string which is being generated
    # with all essential informations in the block.

    def __init__(self, previousBlockHash, hashDifficulty, blockTransactions):
        self.hashDifficulty = hashDifficulty
        self.previousBlockHash = previousBlockHash
        self.blockTransactions = blockTransactions
        self.validationTime = datetime.now().strftime("%H:%M:%S")
        self.blockHash = self.generateBlockHash()
        self.proofOfWork()

    def generateBlockHash(self):
        newhash = self.previousBlockHash + self.validationTime + \
            str(self.blockTransactions) + str(self.blockMineSize)
        return sha256(newhash.encode('utf-8')).hexdigest()

    # This is the mining section. It generates hashes according to the difficulty
    # and guarantees the security of the blockchain with the work done.
    # This section can be improved since continuous increments of blockMineSize
    # is a poor way to generate different hash every turn.

    def proofOfWork(self):
        initialTime = datetime.now()
        while self.blockHash[len(self.blockHash) - self.hashDifficulty:] != "0" * self.hashDifficulty:
            self.blockHash = self.generateBlockHash()
            self.blockMineSize += 1

        finalTime = datetime.now() - initialTime
        print(
            f"Block hash = {self.blockHash}\nmined in {finalTime.total_seconds()} seconds.\n")


class blockchain():
    blockchain = []
    hashDifficulty = 0
    miningReward = 0
    transactions = []
    lastBlockLog = ''

    # We set blockchain's general features.

    def __init__(self, hashDifficulty, miningReward):
        print(f"Mining difficulty is {hashDifficulty}\n")
        self.hashDifficulty = hashDifficulty
        self.miningReward = miningReward
        self.blockchain = [self.createGenesisBlock()]

    # Genesis block is the first node of the blockchain,
    # so, we generated a random string for the starting point(hash).

    def createGenesisBlock(self):
        randomKey = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(30))
        genericTransactions = [transaction("null", "null", 0)]

        # First transaction of the blockchain.

        self.transactions = genericTransactions
        self.validationFlag = True
        return block(sha256(
            randomKey.encode('utf-8')).hexdigest(), self.hashDifficulty, genericTransactions)

    def getCurrentBlock(self):
        return self.blockchain[len(self.blockchain) - 1]

    def newBlock(self, transactions):
        self.validationFlag = self.validateBlockChain()

        if self.validationFlag == True:
            self.blockchain.append(
                block(self.getCurrentBlock().blockHash, self.hashDifficulty, transactions))

    # For security reasons, we will need to validate our blockchain.

    def validateBlockChain(self):
        for i in range(len(self.blockchain) - 1):
            if self.blockchain[i].blockHash != self.blockchain[i + 1].previousBlockHash:
                print("Blockchain isn't valid!!!!.\n")
                self.handleInvalidBlock()
                return False
        return True

    def handleInvalidBlock(self):
        while self.validationFlag == False:
            try:
                self.blockchain.pop()
                print(
                    f"Trying to recover the blockchain to the previous version. Last block index is {len(self.blockchain)}\n")
                self.validateBlockChain()
            except:
                print("There is no block left! Creating a new genesis block..")
                self.blockchain = [self.createGenesisBlock()]
                break
        return

    # This function is responsible for adding transactions to
    # the blockchain and checking them if they are valid.

    def addTransaction(self, newTransaction):
        transactionCoins = self.getBalance(newTransaction.source)

        if newTransaction.coins <= 0:
            self.lastBlockLog = f"Transaction amount can't be a negative value!"
            print(self.lastBlockLog)
            return False

        if transactionCoins < newTransaction.coins:
            self.lastBlockLog = f"Insufficient coins in the source! {newTransaction.source} needs: {newTransaction.coins - transactionCoins}"
            print(self.lastBlockLog)
            return False

        if self.validateTransaction(newTransaction) == False:
            return False

        self.transactions.append(newTransaction)

        # ***Activate this to get only one transaction per block.***
        # self.handleTransaction("null")

        return True

    def addText(self, newText):
        self.transactions.append(newText)

    def forceTransaction(self, newTransaction):
        print(
            f"Transaction is forced. {newTransaction.coins} added to {newTransaction.destination}")
        self.transactions.append(newTransaction)

    def validateTransaction(self, newTransaction):
        signer = digitalSignature()
        transactionHash = signer.validateTransaction(
            newTransaction.transactionSignature)

        if transactionHash == newTransaction.transactionHash:
            print('Transaction is validated!')
            return True
        return False

        # When there is pending transactions, those transactions
        # should be handled by a miner. This is implemented in the
        # function below.

    def handleTransaction(self, miningRewardAddress):
        if len(self.transactions) == 0:
            return False
        work = len(self.transactions)

        # Every block has a limited space for the transactions.

        while len(self.transactions) > self.getCurrentBlock().blockTransactionCapacity:
            limitedTransactions = []
            for i in range(self.getCurrentBlock().blockTransactionCapacity):
                limitedTransactions.append(self.transactions.pop())
            self.newBlock(limitedTransactions)

        if len(self.transactions) != 0:
            self.newBlock(self.transactions)

        self.transactions = []

        # We can change "null" with the user who does the work.

        self.transactions.append(transaction(
            "null", miningRewardAddress, self.miningReward * work))
        return True

    # This function gets the balance of specified address
    # with checking all transactions within the blockchain.

    def getBalance(self, addressofBalance):
        availableCoins = 0

        # With try/catch block, we prevent chat and balance
        # blocks to mix (We cannot mix integers and strings).

        for i in range(len(self.blockchain)):
            for j in range(len(self.blockchain[i].blockTransactions)):
                try:
                    if self.blockchain[i].blockTransactions[j].destination == addressofBalance:
                        availableCoins += self.blockchain[i].blockTransactions[j].coins
                    if self.blockchain[i].blockTransactions[j].source == addressofBalance:
                        availableCoins -= self.blockchain[i].blockTransactions[j].coins
                except:
                    continue

        return availableCoins


# Transaction class saves source and destination
# of the transfers with a validation.

class transaction():
    source = ''
    destination = ''
    coins = 0
    validationTime = None
    transactionHash = ''
    transactionSignature = ''

    def __init__(self, source, destination, coins):
        self.source = source
        self.destination = destination
        self.coins = coins
        self.setTransaction()

    def setTransaction(self):
        self.validationTime = datetime.now().strftime("%H:%M:%S")
        self.generateTransactionHash()

        signer = digitalSignature()
        self.transactionSignature = signer.signTransaction(
            self.transactionHash)

    def generateTransactionHash(self):
        newHash = self.source + self.destination + \
            str(self.coins) + self.validationTime
        self.transactionHash = sha1(newHash.encode('utf-8')).hexdigest()


# We need digital signatures to validate our transactions.
# We can use any asymetric encryption algorithm. For my
# implementation, I will use RSA algorithm.
# ----
# For each transaction, we will encrypt the transaction
# hash and send it to the handler.
# Handler will validate transaction by decrypting the
# hash and compare it with the original transaction
# hash. If they are same, then validation will be done.


class digitalSignature:
    def __init__(self):
        pass

    def signTransaction(self, transactionHash):
        signedHashinBytes = rsa.encrypt(
            transactionHash.encode('utf8'), RSA_PublicKey)

        return signedHashinBytes

    def validateTransaction(self, encryptedTransactionHash):
        validatedHashinBytes = rsa.decrypt(
            encryptedTransactionHash, RSA_PrivateKey)

        return validatedHashinBytes.decode('utf8')


# A general purpose wallet for blockchain.

class wallet():
    ownerName = ''
    publicAddress = ''  # aka source
    privateAddress = ''
    privateKeys = []
    coins = 0
    transactions = []
    creationTime = None

    def __init__(self, ownerName, publicAddress):
        self.ownerName = ownerName
        self.creationTime = datetime.now().strftime("%H:%M:%S")
        self.randomWordGenerator()
        self.generatePublicKey()
        self.generatePrivateKey()
        self.done()

    def generatePublicKey(self):
        stream = self.ownerName + self.creationTime
        self.publicAddress = sha256(stream.encode('utf-8')).hexdigest()

    def generatePrivateKey(self):
        newHash = ""
        for key in self.privateKeys:
            newHash += key
        self.privateAddress = sha256(newHash.encode('utf-8')).hexdigest()

    def randomWordGenerator(self):
        self.privateKeys.append(self.ownerName)
        for i in range(9):
            tempStr = ''
            for j in range(10):
                tempStr += random.choice(string.ascii_lowercase)
            self.privateKeys.append(tempStr)

    def done(self):
        print(
            f'A new public and private key pair is generated for : {self.ownerName}.')
        print(
            'Please write down your private keys in order to keep an access to your transactions and wallet.')
        print(f'Your private keys: {self.privateKeys}\n')
        self.privateKeys.clear()
        # Updating the wallet's owner balance.

    def updateTransactions(self, blockchain):
        coins = blockchain.getBalance(self.ownerName)
        return f'Coins in the wallet: {coins}'


class walletChecker():
    wallets = []

    def __init__(self, wallets):
        self.wallets = wallets

    def addWallet(self, newWallet):
        for wallet in self.wallets:
            if wallet.publicAddress == newWallet.publicAddress:
                print("You can't use an existed wallet name!")
                return

        self.wallets.append(newWallet)


# I used pickle module for saving and loading blockchain database.
# I will also use some encryption techniques here later.
# This database should be transferred with p2p sockets as well.


class database():
    blockchain = None
    wallets = []
    creationDate = None

    def __init__(self):
        self.creationDate = datetime.now().strftime("%H:%M:%S")

    def saveDatabase(self, blockchain, wallets, path):
        save1 = open(path + 'blockchainData1', 'wb')
        pickle.dump(blockchain, save1)
        save2 = open(path + 'walletData1', 'wb')
        pickle.dump(wallets, save2)

        save1.close()
        save2.close()

    def loadDatabase(self, path):
        load1 = open(path + 'blockchainData1', 'rb')
        self.blockchain = pickle.load(load1)
        load2 = open(path + 'walletData1', 'rb')
        self.wallets = pickle.load(load2)

        load1.close()
        load2.close()
