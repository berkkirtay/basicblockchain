from Blockchain import Blockchain
from Wallet import Wallet
from Transaction import Transaction
from BlockchainNode import BlockDataIO

from datetime import datetime
import time
import pathlib

block1 = Blockchain(0, 0.2)  # Mining Difficulty and reward

# Creating two new wallets

wallet1 = Wallet("person1")
wallet1.createNewWallet()

wallet2 = Wallet("person2")
wallet2.createNewWallet()

# Force transaction to person1
block1.forceTransaction(wallet1.publicKey, 10000)

# Handle the pending transaction
block1.handleTransaction(wallet2.publicKey)

# Mining section.

for i in range(5):
    block1.addTransaction(Transaction(
        wallet1.publicKey, wallet2.publicKey, i + 1, wallet1.privateKey))


block1.handleTransaction(wallet2.publicKey)  # Mining reward + 0.2

block1.addTransaction(Transaction(
    wallet1.publicKey, wallet2.publicKey, 10, wallet1.privateKey))
block1.handleTransaction(wallet1.publicKey)

print(block1.getBalance(wallet1.publicKey))  # person1, available coins
print(block1.getBalance(wallet2.publicKey))  # person2, available coins


wallet1.updateTransactions(block1)
wallet2.updateTransactions(block1)
wallets = [wallet1, wallet2]


# Blockchain export and import

pathlib.Path('./blockchain_data').mkdir(exist_ok=True)
BlockDataIO().exportData(block1, "./blockchain_data/blockchainData.json")

block2 = BlockDataIO().readDataAndImport(
    "./blockchain_data/blockchainData.json")
