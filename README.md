# A Proof of Work Based Blockchain Implementation in Python
[![Unit Tests](https://github.com/berkkirtay/basicblockchain/actions/workflows/python-app.yml/badge.svg)](https://github.com/berkkirtay/basicblockchain/actions/workflows/python-app.yml) 
![Coverage](https://img.shields.io/codecov/c/github/berkkirtay/basicblockchain) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**This library lets you initialize a blockchain and perform transactions between peers. This implementation uses the proof of work method to build new blocks. Transactions are signed with a 1024 bit RSA key pair and you can create new wallets with unique key pairs.
I will keep working on this library as I find new features for this implementation.** 

### Current components: 
- Blockchain implementation with user wallets
- Blockchain validators and transaction signatures
- Block mining rewards for block miners
- Export and import module for blockchain data
- Unit tests with GitHub Workflow
- P2P blockchain nodes (Still under development)

### Old Version Components
- Blockchain based voting system and chat module
- Test GUI for basic wallet operations in the old version
 

## Basic Usage 

### Transaction Between Two Peers in Blockchain:

```python
from Blockchain import Blockchain
from Wallet import Wallet
from Transaction import Transaction
# -----------------------------------------------------------------
# Initialize the blockchain:
# Mining Difficulty and reward should be passed as arguments.
# A genesis block will be mined after initialization.

blockchain = Blockchain(2, 1) 
# hashingDifficulty = 2, gasPrice = 1

# -----------------------------------------------------------------
# Creating two new wallets:
# We generate two new user wallets. Wallet will
# generate a new RSA key pair for each user.
# These key pairs will be used to sign and validate transactions.
# A public key defines the address of the user.

wallet1 = Wallet("person1")
wallet2 = Wallet("person2")

# -----------------------------------------------------------------
# Transactions
# Force transaction to person1:

blockchain.forceTransaction(wallet1.publicKey, 1000)

# Transaction between two wallets:
# Sender signs the transaction with his private key and the transaction
# will be validated by its signature to make sure if the sender is the real sender.

blockchain.addTransaction(Transaction(
    wallet1.publicKey, wallet2.publicKey, 10, wallet1.privateKey))

# Sender pays transaction fees to the miner (7).

blockchain.handleTransaction(wallet2.publicKey)

# Updating balances of users:

wallet1.updateTransactions(blockchain)
wallet2.updateTransactions(blockchain)

# wallet1.coins: 983
# wallet2.coins: 17
```

## GUI Screenshots 
In the old version of blockchain, GUI is still available. 

### Wallet Creation
![Enc1](https://github.com/trantorberk/basicblockchain/blob/main/gui_photos/photo1.png)

### Transactions
![Enc1](https://github.com/trantorberk/basicblockchain/blob/main/gui_photos/photo2.png) 

### Mining
![Enc1](https://github.com/trantorberk/basicblockchain/blob/main/gui_photos/photo3.png)
