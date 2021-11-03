from Blockchain import Blockchain
from Wallet import Wallet
from Transaction import Transaction
from DataConverter import BlockDataIO
import random


blockchain = Blockchain(4, 10)

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
        randomWallet1.publicKey, randomWallet2.publicKey, i * i, randomWallet1.privateKey))

blockchain.handleTransaction("null")

# Blockchain data export and import

wallets[1].updateTransactions(blockchain)
userBalanceBeforeExport = wallets[1].coins

BlockDataIO().exportData(blockchain, "blockchainData.json")
block2 = BlockDataIO().readDataAndImport("blockchainData.json")
BlockDataIO().exportData(block2, "blockchainData2.json")

wallets[1].updateTransactions(blockchain)
userBalanceAfterExport = wallets[1].coins

if userBalanceBeforeExport == userBalanceAfterExport:
    print("Success")
