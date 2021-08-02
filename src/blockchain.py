# This is my first blockchain implementation.
# There can be many bugs or wrong approaches,
# please check the potential bugs before using!

from hashlib import sha256
from os import error
from datetime import datetime
import random
import string
import pickle

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
        while self.blockHash[len(self.blockHash) - self.hashDifficulty:] != "a" * self.hashDifficulty:
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
        return block(sha256(randomKey.encode('utf-8')).hexdigest(), self.hashDifficulty, genericTransactions)

    def getCurrentBlock(self):
        return self.blockchain[len(self.blockchain) - 1]

    def newBlock(self, transactions):
        self.validationFlag = self.validateBlockChain()
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
        if newTransaction.coins <= 0 or transactionCoins < newTransaction.coins:
            self.lastBlockLog = f"Insufficient coins in the source! {newTransaction.source} needs: {newTransaction.coins - transactionCoins}"
            print(self.lastBlockLog)
            return False
        else:
            self.transactions.append(newTransaction)
            self.handleTransaction("null")  # Attention here!
            return True

    def forceTransaction(self, newTransaction):
        print(
            f"Transaction is forced. {newTransaction.coins} added to {newTransaction.destination}")
        self.transactions.append(newTransaction)
        return True

    # When there is pending transactions, those transactions
    # should be handled by a miner. This is implemented in the
    # function below.
    def handleTransaction(self, miningRewardAddress):
        if len(self.transactions) == 0:
            return False
        work = len(self.transactions)

        # Every block has a limited space for transactions.
        while len(self.transactions) > self.getCurrentBlock().blockTransactionCapacity:
            limitedTransactions = []
            for i in range(self.getCurrentBlock().blockTransactionCapacity):
                limitedTransactions.append(self.transactions.pop())
            self.newBlock(limitedTransactions)

        if len(self.transactions) != 0:
            self.newBlock(self.transactions)

        self.transactions = []
        self.transactions.append(transaction(
            "null", miningRewardAddress, self.miningReward * work))
        return True

    # This function gets the balance of specified address
    # with checking all transactions within the blockchain.
    def getBalance(self, addressofBalance):
        availableCoins = 0
        for i in range(len(self.blockchain)):
            for j in range(len(self.blockchain[i].blockTransactions)):
                if self.blockchain[i].blockTransactions[j].destination == addressofBalance:
                    availableCoins += self.blockchain[i].blockTransactions[j].coins
                if self.blockchain[i].blockTransactions[j].source == addressofBalance:
                    availableCoins -= self.blockchain[i].blockTransactions[j].coins

        return availableCoins

# Transaction class saves source and destination
# of the transfers with a validation.


class transaction():
    source = ''
    destination = ''
    coins = 0
    validationTime = None
    transactionHash = ''

    def __init__(self, source, destination, coins):
        self.source = source
        self.destination = destination
        self.coins = coins
        self.validationTime = datetime.now().strftime("%H:%M:%S")
        self.transactionHash = self.generateTransactionHash()

    def generateTransactionHash(self):
        newHash = self.source + self.destination + \
            str(self.coins) + self.validationTime
        return sha256(newHash.encode('utf-8')).hexdigest()


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
        self.publicAddress = sha256(self.ownerName.encode('utf-8')).hexdigest()

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

        # Updating the wallet's owner balance.

    def updateTransactions(self, blockchain):
        coins = blockchain.getBalance(self.ownerName)
        return f'Coins in the wallet: {coins}'

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

# block1 = blockchain(4,0.2) # Mining Difficulty and reward
