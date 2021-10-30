# This script hasn't been done yet..

from hashlib import new
import socket
import threading
import pickle
import time
from Blockchain import *


class p2p():
    # This is not completely a p2p network but any client can act like a server
    # and transfer updated blockchain information to other peers.
    blockchain = None
    address = ''
    PORT = 0
    socket1 = None
    continuousTransfer = True

    def __init__(self, blockchain, address, PORT):
        self.blockchain = blockchain
        if self.blockchain == None:
            print("Getting blockchain..\n")
        self.address = address
        self.PORT = PORT
        self.socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handleNetwork()

    def handleNetwork(self):
        if self.socket1.connect_ex((self.address, self.PORT)) == 0:
            self.addPair()
        else:
            self.socket1.bind((self.address, self.PORT))
            self.startNetwork()

    def handleNewConnection(self, newConnection, newAddress):
        print(f"New connection: {newAddress}")
        try:
            data = pickle.dumps(self.blockchain)
            newConnection.send(data)
            data = self.newConnection.recv(10000)
            self.blockchain = pickle.loads(data)
           # self.refreshBlockchain()
        except:
            print(f"Peer is down: {newAddress}")
            newConnection.close()
        print(f"Blockchain data is transferred to {newAddress}")
        newConnection.close()

    def startNetwork(self):
        self.socket1.listen()
        # We listen for new peers continuously
        while self.continuousTransfer:
            try:
                newConnection, newAddress = self.socket1.accept()
                newthread = threading.Thread(
                    target=self.handleNewConnection, args=(newConnection, newAddress))
                newthread.start()
            except KeyboardInterrupt:
                self.stopNetwork()
                break
            #self.continuousTransfer = False

    def addPair(self):
        try:
            data = pickle.dumps(self.blockchain)
            self.socket1.send(data)
            data = self.socket1.recv(10000)
            self.blockchain = pickle.loads(data)
        except:
            self.socket1.close()
           # self.handleNetwork()

    def refreshBlockchain(self, blockchain):
       # data = self.socket1.recv(100000)
        #self.blockchain = pickle.loads(data)
        self.blockchain = blockchain
        data = pickle.dumps(self.blockchain)
        self.socket1.send(data)

    def stopNetwork(self):
        self.continuousTransfer = False
        self.socket1.close()
