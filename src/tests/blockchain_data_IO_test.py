from Blockchain import Blockchain
from Wallet import Wallet
from Transaction import Transaction
from DataConverter import BlockDataIO
import random
import pytest

blockchain = Blockchain(1, 10)

# Creating random wallets

wallets = []
for i in range(1, 25):
    newWallet = Wallet("null")
    newWallet.createNewWallet()
    wallets.append(newWallet)
    blockchain.forceTransaction(newWallet.publicKey, 100000000)

blockchain.handleTransaction("null")

for i in range(1, 500):
    randomWallet1 = wallets[random.randint(0, 23)]
    randomWallet2 = wallets[random.randint(0, 23)]
    blockchain.addTransaction(Transaction(
        randomWallet1.publicKey, randomWallet2.publicKey, random.randint(1, 1000), randomWallet1.privateKey))

blockchain.handleTransaction("null")

# Blockchain data export and import
userBalanceBeforeExport = 0
userBalanceAfterExport = 0

for i in range(1, 24):
    wallets[i].updateTransactions(blockchain)
    userBalanceBeforeExport += wallets[i].getBalance(blockchain)

BlockDataIO().exportData(blockchain, "blockchainData.json")
blockchain2 = BlockDataIO().readDataAndImport("blockchainData.json")

for i in range(1, 24):
    wallets[i].updateTransactions(blockchain2)
    userBalanceAfterExport = wallets[i].getBalance(blockchain2)

# userBalanceBeforeExport == userBalanceAfterExport
print(f"{userBalanceBeforeExport} ve {userBalanceAfterExport}")
