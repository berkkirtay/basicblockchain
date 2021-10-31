from Blockchain import Blockchain
from Wallet import Wallet
from Transaction import Transaction

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
wallet1.createNewWallet()

wallet2 = Wallet("person2")
wallet2.createNewWallet()

# Transactions


# Force transaction to person1:
blockchain.forceTransaction(wallet1.publicKey, 10000)

# Mine the pending transaction:
blockchain.handleTransaction(wallet2.publicKey)

for i in range(1, 10):
    blockchain.addTransaction(Transaction(
        wallet1.publicKey, wallet2.publicKey, i * i, wallet1.privateKey))

# Miner gains the block mining rewards.
blockchain.handleTransaction(wallet2.publicKey)

# Transaction between two wallets:

blockchain.addTransaction(Transaction(
    wallet1.publicKey, wallet2.publicKey, 10, wallet1.privateKey))

blockchain.handleTransaction(wallet1.publicKey)

# Updating balances of users:
wallet1.updateTransactions(blockchain)
wallet2.updateTransactions(blockchain)

person1Balance = wallet1.coins  # 10000 - 295 = 9705
person2Balance = wallet2.coins  # 295 + 10*2 = 315

print(f"Balance of person1: {person1Balance}")
print(f"Balance of person2: {person2Balance}")
