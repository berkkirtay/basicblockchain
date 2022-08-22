'''
MIT License

Copyright (c) 2022 Berk Kırtay

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

# ------------------------------------------------------------------
# This program is a basic and easy to use blockchain implementation.
# There can be bugs or uncovered parts in unit tests.
# Please be aware of the potential risks before using!
# Developed by Berk Kırtay, all source code is under MIT License.
# ------------------------------------------------------------------


from src.BlockchainExceptionHandler.BlockchainExceptionHandler import *
from src.BlockchainLogger.BlockchainLogger import initializeLogger, logging
from src.Transaction.Transaction import Transaction
from src.Transaction.TransactionSignature import TransactionSignature, generateGenesisSignerKeyPair
from Crypto.Hash import SHA256
from datetime import datetime
import random
import string


class GenesisBlockKeyProvider():
    GENESIS_BLOCK_PRIVATE_KEY = ""
    GENESIS_BLOCK_PUBLIC_KEY = ""

    def __init__(self):
        key_pair = generateGenesisSignerKeyPair()
        self.GENESIS_BLOCK_PUBLIC_KEY = key_pair[0]
        self.GENESIS_BLOCK_PRIVATE_KEY = key_pair[1]

    def private_key(self) -> str:
        return self.GENESIS_BLOCK_PRIVATE_KEY

    def public_key(self) -> str:
        return self.GENESIS_BLOCK_PUBLIC_KEY


KEY_PAIR = None

initializeLogger()

# Every block keeps previous block's hash for validation between blocks.
# We create a hash code based on previous block's hash,
# block's validation time and transactions.
# This method is basically bitcoin's consensus approach


class Block():
    previousBlockHash = ''
    blockHash = ''
    blockNonce = 0
    hashDifficulty = 0
    blockBalance = 0
    blockFee = 0
    validationTime = None
    blockTransactionCapacity = 1000
    blockTransactions = []

    # Each block has its unique hash string which is being generated
    # with all the essential information in the block.

    def __init__(self, previousBlockHash: str, hashDifficulty: int, blockTransactions: list):
        self.hashDifficulty = hashDifficulty
        self.previousBlockHash = previousBlockHash
        self.blockTransactions = blockTransactions
        self.validationTime = datetime.now().strftime("%H:%M:%S")
        self.calculateBlockFeeAndBalance()
        self.blockHash = self.generateBlockHash()
        self.proofOfWork()

    def generateBlockHash(self):
        stream = str(self.previousBlockHash) + self.validationTime + \
            str(self.blockTransactions) + str(self.blockNonce)
        return SHA256.new(stream.encode('utf-8')).hexdigest()

    # This is the block mining section. It generates hashes according to the difficulty
    # and guarantees the security of the blockchain with the work done.
    # This section can be improved since continuous increments of blockNonce
    # is a poor way to generate different hash every turn.

    def proofOfWork(self):
        initialTime = datetime.now()
        while self.blockHash[:self.hashDifficulty] != "0" * self.hashDifficulty:
            self.blockNonce += 1
            self.blockHash = self.generateBlockHash()

        finalTime = datetime.now() - initialTime
        logging.info(
            f"Block hash = {self.blockHash} is mined in {finalTime.total_seconds()} seconds.")

    def calculateBlockFeeAndBalance(self):
        for transaction in self.blockTransactions:
            self.blockFee += transaction.fee
            self.blockBalance += transaction.balance


class Blockchain():
    blockchain = []
    hashDifficulty = 0
    gasPrice = 0
    chainSize = 0
    pendingTransactions = []
    lastBlockLog = ''

    # Setting up blockchain's general features.

    def __init__(self, hashDifficulty: int, gasPrice: int = 1):
        self.hashDifficulty = hashDifficulty
        self.gasPrice = gasPrice
        self.blockchain = [self.createGenesisBlock()]
        logging.info("Blockchain has been initialized...")
        logging.info(
            f"Block hashing difficulty is {hashDifficulty}. Block fee rate is {gasPrice}.")
        logging.info(
            f"Block Transaction capacity is {self.blockchain[-1].blockTransactionCapacity}")

        logging.info("Genesis block is initialized successfully.")

    # Genesis block is the first node of the blockchain,
    # so, we generated a random string for the starting point(hash).

    def createGenesisBlock(self):
        randomKey = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(30))

        global KEY_PAIR
        KEY_PAIR = GenesisBlockKeyProvider()

        genericTransaction = Transaction(
            KEY_PAIR.public_key(), "null", 0, KEY_PAIR.private_key())
        genericTransaction.approve()
        genericTransactions = [genericTransaction]

        self.validationFlag = True
        return Block(SHA256.new(randomKey.encode('utf-8')).hexdigest(),
                     self.hashDifficulty, genericTransactions)

    def getCurrentBlock(self):
        return self.blockchain[-1]

    def mineNewBlock(self, transactions: list):
        self.insertBlockAndReevaluateDifficulty(
            Block(self.getCurrentBlock().blockHash, self.hashDifficulty, transactions))

        self.validateBlockchain()

    # Blockchain will make mining harder as it has more blocks.
    # This is a similar procedure for all other famous blockchain applications.
    # To be more precise, this implementation should be changed based on
    # peer numbers who actively mine blocks. I will change this
    # feature once I implement peer to peer network properly.

    def insertBlockAndReevaluateDifficulty(self, newBlock: Block):
        self.blockchain.append(newBlock)
        self.chainSize += 1
        if self.hashDifficulty == 0:
            return

        while True:
            difficultyDeterminer = (self.chainSize / self.hashDifficulty) / 10
            if difficultyDeterminer < 10:
                break
            else:
                self.hashDifficulty += 1

    # To secure our blocks, we need to validate our blockchain.
    # We do that by simply checking hash data of the blocks.

    def validateBlockchain(self):
        for i in range(len(self.blockchain) - 1):
            try:
                validationHash = self.blockchain[i].generateBlockHash()
                if validationHash != self.blockchain[i].blockHash:
                    self.validationFlag = False
                    raise IllegalAccessError()

                if self.blockchain[i].blockHash != self.blockchain[i + 1].previousBlockHash:
                    self.validationFlag = False
                    raise BlockchainSequenceError(
                        "Blockchain sequence isn't valid!")
            except IllegalAccessError:
                self.lastBlockLog = "Changed block properties found!" + \
                    "The corresponding block is corrupted! You may switch to a backup mirror blockchain."
                logging.critical(f"IllegalAccessError: {self.lastBlockLog}")
                raise IllegalAccessError(
                    "Changed block properties found! The corresponding block is corrupted!")
            except BlockchainSequenceError:
                self.handleInvalidBlock()

        self.validationFlag = True

    def handleInvalidBlock(self):
        while self.validationFlag == False:
            try:
                self.blockchain.pop()
                self.lastBlockLog = f"Trying to recover the blockchain to the previous version. Last block index is {len(self.blockchain)}\n"
                logging.WARNING(
                    f"BlockchainSequenceError: {self.lastBlockLog}")
                self.validateBlockchain()
            except:
                self.lastBlockLog = "There is no block left! Creating a new genesis block.."
                logging.critical(f"IllegalAccessError: {self.lastBlockLog}")
                self.blockchain = [self.createGenesisBlock()]
                break
        return

    # This function is responsible for adding transactions to
    # the blockchain and checking them if they are valid.

    def addTransaction(self, newTransaction: Transaction):
        # With this type checking, we prevent str and int
        # blocks to mix (We cannot mix integers and strings).
        if type(newTransaction.balance) is not int:
            raise TransactionDataConflictError()

        newTransaction.calculateTransactionFee(self.gasPrice)
        transactionBalance = self.getBalance(newTransaction.source)

        if newTransaction.balance <= 0:
            self.lastBlockLog = "Transaction amount can't be zero or a negative value!"
            logging.warning(self.lastBlockLog)
            raise BalanceError(self.lastBlockLog)

        if transactionBalance < newTransaction.balance:
            self.lastBlockLog = f"Insufficient balance in the source! {newTransaction.source} needs: {newTransaction.balance  - transactionBalance}"
            logging.warning(self.lastBlockLog)
            raise BalanceError("Insufficient balance in the source!")

        self.pendingTransactions.append(newTransaction)
        logging.info(
            f"A new transaction has been added to blockchain.")  # by {newTransaction.source}

        # ***Activate this to get only one transaction per block.***
        # self.handleTransaction("null")

    # Forcing transactions is only for testing. It creates a
    # transaction with the genesis block's signature.

    def forceTransaction(self, publicAddress: str, balance: float):
        newTransaction = Transaction(KEY_PAIR.public_key(),
                                     publicAddress,
                                     balance,
                                     KEY_PAIR.private_key())

        self.pendingTransactions.append(newTransaction)
        self.handleTransactions(KEY_PAIR.public_key())

        logging.info(
            f"A forced transaction is added to the chain. Amount: {balance}")

    # When there is pending transactions, those transactions
    # should be handled by a miner. This is implemented in the
    # function below.

    def handleTransactions(self, rewardAddress: str):
        # Every block has a limited space for the transactions.
        self.validateBlockchain()
        while not len(self.pendingTransactions) == 0:
            limitedTransactions = []
            transactionsSize = 0

            if self.getCurrentBlock().blockTransactionCapacity > len(self.pendingTransactions):
                transactionsSize = len(self.pendingTransactions)
            else:
                transactionsSize = self.getCurrentBlock().blockTransactionCapacity

            currentReward = 0
            for i in range(transactionsSize):
                nextTransaction = self.pendingTransactions.pop()
                isValid = self.validateTransaction(
                    nextTransaction, nextTransaction.source)

                if isValid == True:
                    nextTransaction.approve()
                    limitedTransactions.append(nextTransaction)
                    currentReward += nextTransaction.fee

                # else:
                # TODO
                # Blockchain can add invalid transactions to a blacklist
                # to prevent the fraud wallet users form using blockchain again.

            # Block rewards are paid from transaction fees.
            # To sign block reward transactions, we use a pregenerated
            # genesis key pair. This key pair is the authorized to
            # give block rewards and force transactions to test blockchain.

            if rewardAddress != KEY_PAIR.public_key():
                blockReward = Transaction(
                    KEY_PAIR.public_key(),
                    rewardAddress,
                    currentReward,
                    KEY_PAIR.private_key())

                blockReward.approve()
                limitedTransactions.append(blockReward)

            self.mineNewBlock(limitedTransactions.copy())

    def validateTransaction(self, newTransaction: Transaction, publicKey: str):
        transactionSigner = TransactionSignature()
        validator = transactionSigner.validateTransaction(
            newTransaction.transactionHash, newTransaction.transactionSignature, publicKey)

        if validator == True:
            logging.info(
                f'Transaction is validated! -> {newTransaction.transactionHash.hexdigest()}')
            return True
        return False

    # This function gets the balance of specified address
    # with checking all Transactions within the blockchain.

    def getBalance(self, addressofBalance: str):
        availableBalance = 0

        for i in range(len(self.blockchain)):
            for j in range(len(self.blockchain[i].blockTransactions)):
                if self.blockchain[i].blockTransactions[j].destination == addressofBalance:
                    availableBalance += self.blockchain[i].blockTransactions[j].balance
                if self.blockchain[i].blockTransactions[j].source == addressofBalance:
                    availableBalance -= (self.blockchain[i].blockTransactions[j].balance +
                                         self.blockchain[i].blockTransactions[j].fee)

        # Check if current source has any pending transaction.

        for transaction in self.pendingTransactions:
            if transaction.destination == addressofBalance:
                availableBalance += transaction.balance
            if transaction.source == addressofBalance:
                availableBalance -= (transaction.balance + transaction.fee)

        return availableBalance
