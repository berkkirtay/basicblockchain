from Blockchain import Blockchain
from Wallet import Wallet
from Transaction import Transaction
from DataConverter import BlockDataIO


block1 = Blockchain(3, 10)

# Creating two new wallets

wallet1 = Wallet("person1")
wallet1.createNewWallet()

block1.forceTransaction(wallet1.publicKey, 1000000000)

block1.handleTransaction("null")

for i in range(1, 300):
    block1.addTransaction(Transaction(
        wallet1.publicKey, "null", i * i, wallet1.privateKey))
    if i % 10 == 0:
        block1.handleTransaction(wallet1.publicKey)


# Blockchain export and import

wallet1.updateTransactions(block1)

userBalanceBeforeExport = wallet1.coins

BlockDataIO().exportData(block1, "blockchainData.json")
block2 = BlockDataIO().readDataAndImport("blockchainData.json")
BlockDataIO().exportData(block2, "blockchainData2.json")

wallet1.updateTransactions(block1)
userBalanceAfterExport = wallet1.coins

if userBalanceBeforeExport == userBalanceAfterExport:
    print("Success")
