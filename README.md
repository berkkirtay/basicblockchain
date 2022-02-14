# Basic Blockchain Implementation 
[![Unit Tests](https://github.com/berkkirtay/basicblockchain/actions/workflows/python-app.yml/badge.svg)](https://github.com/berkkirtay/basicblockchain/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A functional blockchain implementation in python. This library lets you initialize a blockchain and perform transactions between peers. This implementation uses the proof of work method to build new blocks. Transactions are signed with a 1024 bit RSA key pair and you can create new wallets with unique key pairs.
I will keep improving this library as I learn more about blockchain technology.

### Current components: 
- Blockchain implementation with user wallets
- Blockchain validators and transaction signatures
- P2P blockchain nodes (Still under development)
- Basic export and import module for blockchain data
- Blockchain based voting system and chat module
- Test GUI for basic wallet operations 
 

## Basic Usage 

### Transaction Between Two Peers in Blockchain:

```python
# Imports![badge](https://user-images.githubusercontent.com/56089152/153960292-112b658a-ff38-4e8c-984f-947a82185cf9.svg)

from Blockchain import Blockchain
from Wallet import Wallet
from Transaction import Transaction
# -----------------------------------------------------------------
# Initialize the blockchain:

# Mining Difficulty and reward shuld be passed as arguments.
# A genesis block will be mined after initialization.
blockchain = Blockchain(2, 10)

# -----------------------------------------------------------------
# Creating two new wallets:

# We generate two new user wallets. Wallet will
# generate new RSA key pair for each user.
# These key pairs will be used as to sign and validate transactions.
# A public key defines the address of the user.
wallet1 = Wallet("person1")
wallet2 = Wallet("person2")

# -----------------------------------------------------------------
# Transactions

# Force transaction to person1:
blockchain.forceTransaction(wallet1.publicKey, 1000)

# Mine the pending transaction:
blockchain.handleTransaction(wallet2.publicKey)

# Transaction between two wallets:
# Sender signs the transaction with his private key and this 
# signature will be validated to make sure if the sender is the real sender.
blockchain.addTransaction(Transaction(
    wallet1.publicKey, wallet2.publicKey, 10, wallet1.privateKey))

# Miner gains the block mining rewards.
blockchain.handleTransaction(wallet2.publicKey)

# Updating balances of users:
wallet1.updateTransactions(blockchain)
wallet2.updateTransactions(blockchain)

# wallet1.coins: 990
# wallet2.coins: 30
```

## GUI Screenshots 
In the old version of blockchain, GUI is still available. 

### Wallet Creation
![Enc1](https://github.com/trantorberk/basicblockchain/blob/main/gui_photos/photo1.png)

### Transactions
![Enc1](https://github.com/trantorberk/basicblockchain/blob/main/gui_photos/photo2.png) 

### Mining
![Enc1](https://github.com/trantorberk/basicblockchain/blob/main/gui_photos/photo3.png)
