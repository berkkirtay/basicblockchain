# Copyright (c) 2022 Berk Kırtay

from src.Blockchain.Blockchain import Blockchain
from src.Wallet.Wallet import Wallet
from src.Transaction.Transaction import Transaction
from src.DataConverter.DataConverter import BlockDataIO
import pytest

# Blockchain initialization

# Mining Difficulty and reward
blockchain = Blockchain(2, 10)

# Creating two new wallets:

# Each wallet has a user name. createNewWallet function
# generates cryptographic key pair for the wallet user.
# This unique key pair will be used for transactions.
# Users will be defined by their public key and sign
# their transactions with their private key.

wallet1 = Wallet("person1")
wallet2 = Wallet("person2")

# Transactions


# Force transaction to person1:
blockchain.forceTransaction(wallet1.publicKey, 10000)

# wallet1 sends 295 coins to wallet2.
for i in range(1, 10):
    blockchain.addTransaction(Transaction(
        wallet1.publicKey, wallet2.publicKey, i * i, wallet1.privateKey))

# Miner gains the block mining rewards.
blockchain.handleTransactions(wallet2.publicKey)

# Transaction between two wallets:

blockchain.addTransaction(Transaction(
    wallet1.publicKey, wallet2.publicKey, 10, wallet1.privateKey))

blockchain.handleTransactions(wallet2.publicKey)

# Updating balances of users:
wallet1.updateTransactions(blockchain)
wallet2.updateTransactions(blockchain)

person1Balance = wallet1.coins  # 10000 - 295 = 9705
person2Balance = wallet2.coins  # 295 + 10*2 = 315

print(f"Balance of person1: {person1Balance}")
print(f"Balance of person2: {person2Balance}")


def test_walletsShouldHaveCorrectBalances():
    assert person1Balance == 9705
    assert person2Balance == 315
