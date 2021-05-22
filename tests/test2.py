from blockchain import *
from p2pserver import *
import socket
import threading
import pickle
import time


newNetwork = p2p(None, socket.gethostbyname(socket.gethostname()), 8000)
block1 = newNetwork.blockchain

def printBlockchain(blockchain):
    for i in range(len(blockchain.blockchain)):
        print(f'{i + 1}. block: {blockchain.blockchain[i].blockHash}, {blockchain.blockchain[i].validationTime}\n')

printBlockchain(block1)