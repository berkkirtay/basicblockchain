# Copyright (c) 2022 Berk Kırtay

from src.Blockchain.Blockchain import Blockchain
from src.Wallet.Wallet import Wallet
from src.Transaction.Transaction import Transaction
from src.DataConverter.DataConverter import BlockDataIO
import random


blockchain = Blockchain(3, 10)

# Creating random wallets

wallets = []
for i in range(25):
    newWallet = Wallet("person")
    wallets.append(newWallet)
    blockchain.forceTransaction(newWallet.publicKey, 100000000)

for i in range(1, 200):
    randomWallet1 = wallets[random.randint(0, 24)]
    randomWallet2 = wallets[random.randint(0, 24)]
    blockchain.addTransaction(Transaction(
        randomWallet1.publicKey, randomWallet2.publicKey, random.randint(1, 1000), randomWallet1.privateKey))

blockchain.handleTransactions(wallets[0].publicKey)

# Blockchain data export and import
usersBalanceBeforeExport = 0
usersBalanceAfterExport = 0

for i in range(25):
    wallets[i].updateTransactions(blockchain)
    usersBalanceBeforeExport += wallets[i].getBalance(blockchain)

BlockDataIO().exportData(blockchain, "blockchainData.json")
blockchain2 = BlockDataIO().importData("blockchainData.json")

for i in range(25):
    wallets[i].updateTransactions(blockchain2)
    usersBalanceAfterExport += wallets[i].getBalance(blockchain2)


def test_usersBalancesBeforeAndAfterIOMustBeEqual():
    assert usersBalanceBeforeExport == usersBalanceAfterExport
