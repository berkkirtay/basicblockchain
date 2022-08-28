# ---------------------------------------------------
# Transaction class handles transaction data between
# peers. It also provides digital signatures for each
# transaction.
# Copyright (c) 2022 Berk Kırtay
# ---------------------------------------------------

from datetime import datetime
from Crypto.Hash import SHA256
import base64
from src.Transaction.TransactionSignature import TransactionSignature


class Transaction:
    source = ''
    destination = ''
    balance = 0
    gas = 0
    fee = 0
    transactionMessage = ''
    transactionHash = ''
    transactionSignature = ''
    validationTime = None
    isNew = True

    @classmethod
    def initializeTransaction(self, source: str, destination: str, balance: float,
                              gas: int, fee: int, transactionMessage: str, transactionHash: str,
                              transactionSignature: str, validationTime: str):
        self.gas = gas
        self.fee = fee
        self.transactionMessage = transactionMessage
        self.transactionHash = transactionHash
        self.transactionSignature = transactionSignature
        self.validationTime = validationTime
        self.isNew = False
        return self(source, destination, balance, None)

    def __init__(self, source: str, destination: str,
                 balance: float, sourcePrivateKey: str,
                 transactionMessage=None):
        self.source = source
        self.destination = destination
        self.balance = balance
        if transactionMessage == None:
            self.transactionMessage = f"Transaction value: {balance}, sent by {source} to {destination}"
        if self.isNew == True:
            self.setTransaction(sourcePrivateKey)

    def setTransaction(self, sourcePrivateKey: str):
        self.validationTime = datetime.now().strftime("%H:%M:%S")
        self.generateTransactionHash()

        transactionSigner = TransactionSignature()
        self.transactionSignature = transactionSigner.signTransaction(
            self.transactionHash, sourcePrivateKey)

    def generateTransactionHash(self):
        stream = self.source + self.destination + \
            str(self.balance) + self.validationTime
        self.transactionHash = SHA256.new(stream.encode("utf-8"))

    def approve(self):
        self.transactionHashByte = self.transactionHash
        self.transactionHash = self.transactionHash.hexdigest()
        self.transactionSignature = base64.b64encode(
            self.transactionSignature).decode("ascii")

    def calculateTransactionFee(self, gasPrice: int):
        self.gas = len(str(self.balance)) + \
            round(len(self.transactionMessage) / 100)
        self.fee = self.gas * gasPrice
