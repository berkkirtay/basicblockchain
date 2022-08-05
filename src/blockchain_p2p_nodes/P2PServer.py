# ----------------------------------------
# Copyright (c) 2022 Berk Kırtay
# This module is still under development.
# ----------------------------------------

from hashlib import new
import socket
import threading
import asyncio
import time
from Blockchain import *
from DataConverter import DataConverter


class P2PServer():
    blockchain = None
    address = ''
    PORT = 7500
    socket = None
    continuousTransfer = True

    def __init__(self, address, PORT):
        self.address = address
        self.PORT = PORT

    async def addBlockchainData(self, blockchain):
        self.blockchain = blockchain
        self.setNetworkPreferences()
        await self.initializeNetwork()

    def setNetworkPreferences(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = socket.gethostname()

    async def initializeNetwork(self):
        try:
            self.socket.connect((self.address, self.PORT))
            print("Connected to network!")
            while self.continuousTransfer == True:
                data = self.socket.recv(1024 * 64).decode("utf-8")
                receivedBlockchain = self.getBlockchainDataAsObject(data)
                print("Blockchain data is recevied!")

                if len(receivedBlockchain.blockchain) > len(self.blockchain.blockchain):
                    self.blockchain = receivedBlockchain
                else:
                    data = self.getBlockchainDataAsBytes()
                    self.socket.send(data)
                    print("New blockchain data is sent to peers")

                time.sleep(10)

        except Exception as err:
            print(err)
            self.socket.close()
            self.setNetworkPreferences()
            self.socket.bind((self.address, self.PORT))
            await self.listenForPeers()

    async def listenForPeers(self):
        self.socket.listen(10)
        print("Listening for peers..")
        while self.continuousTransfer:
            try:
                newConnection, newAddress = self.socket.accept()
                newthread = threading.Thread(
                    target=self.handleNewConnection, args=(newConnection, newAddress))
                newthread.start()
                #self.handleNewConnection(newConnection, newAddress)
            except KeyboardInterrupt:
                newConnection.close()
                self.stopNetwork()
                break

    def handleNewConnection(self, newConnection, newAddress):
        print(f"New request by: {newAddress}")
        try:
            data = self.getBlockchainDataAsBytes()
            newConnection.send(data)
            print("Blockchain data is sent!")

            receivedData = newConnection.recv(1024 * 16).decode("utf-8")
            receivedBlockchain = self.getBlockchainDataAsObject(receivedData)

            if len(receivedBlockchain.blockchain) > len(self.blockchain.blockchain):
                self.blockchain = receivedBlockchain

        except Exception as err:
            print(f"Peer: {err}")
            newConnection.close()

        print(f"Request is handled with {newAddress}")
        # newConnection.close()

    def getBlockchainDataAsBytes(self) -> bytes:
        blockchainData = DataConverter().dumBlochcainDataAsStr(self.blockchain)
        return bytes(blockchainData, encoding='utf8')

    def getBlockchainDataAsObject(self, data) -> Blockchain:
        return DataConverter().loadBlockchainData(data)

    def stopNetwork(self):
        self.continuousTransfer = False
        self.socket.close()
