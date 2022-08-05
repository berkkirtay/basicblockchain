# Copyright (c) 2022 Berk Kırtay

from Blockchain import *
from Wallet import *
from Transaction import Transaction
from DataConverter import *
from P2PServer import P2PServer


from hashlib import new
import asyncio
import time

# TODO


class Node:
    blockchain = None
    network = None
    nodePublicAddress = None

    def __init__(self, public_key):
        self.nodePublicAddress = public_key

    def initializeNode(self):
        self.network = P2PServer(None, 8001)
        self.blockchain = Blockchain(2, 3)
        asyncio.run(self.network.addBlockchainData(self.blockchain))

    def mineBlock(self):
        self.blockchain.handleTransaction(self.nodePublicAddress)

    def sendUpdatedBlockchain(self):
        asyncio.run(self.network.addBlockchainData(self.blockchain))

    def receiveUpdatedBlockchain(self):
        self.blockchain = self.network.blockchain

    def sendTransaction(self, transaction):
        self.blockchain.addTransaction(transaction)
        self.sendUpdatedBlockchain()


wallet = Wallet("berk")
wallet.createNewWallet()

node = Node(wallet.publicKey)
node.initializeNode()
node.blockchain.forceTransaction(wallet.publicKey, 1000)
node.mineBlock()
node.sendTransaction(Transaction(
    wallet.publicKey, "kimse", 1000, wallet.privateKey))
node.mineBlock()
