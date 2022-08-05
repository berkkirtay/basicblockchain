# ----------------------------------------
# A general purpose wallet for blockchain.
# Copyright (c) 2022 Berk Kırtay
# ----------------------------------------

from src.Blockchain.Blockchain import Blockchain
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import json
import pathlib
import logging

class Wallet():
    ownerName = ''
    publicKey = ''  # aka source
    privateKey = ''
    balance = 0
    creationTime = None
    keySize = 1024

    def __init__(self, ownerName: str):
        self.ownerName = ownerName
        self.createNewWallet()

    def createNewWallet(self):
        self.creationTime = datetime.now().strftime("%H:%M:%S")
        self.generateKeyPair()
        self.exportKeyPair()
        self.done()

    def generateKeyPair(self):
        randomGenerator = Random.new().read
        keyPair = RSA.generate(self.keySize, randomGenerator)
        privateKey = keyPair.exportKey('PEM')
        self.privateKey = base64.b64encode(privateKey).decode("ascii")

        publicKey = keyPair.publickey().exportKey('PEM')
        self.publicKey = base64.b64encode(publicKey).decode("ascii")

        # Here we shorten public key by removing the trivial parts.
        self.publicKey = self.publicKey[87:-44]

    def exportKeyPair(self):
        keypair = {
            "wallet_user_name": self.ownerName,
            "private_key": self.privateKey
        }
        pathlib.Path('./key_pair_exports').mkdir(exist_ok=True)
        with open('./key_pair_exports/' + self.ownerName + '_key_pair.json', 'w', encoding='utf-8') as f:
            json.dump(keypair, f, ensure_ascii=False, indent=4)

    @classmethod
    def importWallet(self, ownerName):
        keypair = dict()
        pathlib.Path('./key_pair_exports').mkdir(exist_ok=True)
        with open('./key_pair_exports/' + ownerName + '_key_pair.json', 'r', encoding='utf-8') as f:
            keypair = json.load(f)

        keyPair = RSA.import_key(base64.b64decode(keypair["private_key"]))
        private_key = keyPair.export_key('PEM')
        public_key = keyPair.publickey().exportKey('PEM')

        wallet = Wallet(ownerName)

        wallet.privateKey = base64.b64encode(private_key).decode("ascii")
        wallet.publicKey = base64.b64encode(public_key).decode("ascii")
        wallet.publicKey = wallet.publicKey[87:-44]

        logging.info(f"Wallet: A new wallet named {ownerName} is imported.")
        return wallet

    def done(self):
        logging.info(
            f'Wallet: A new public and private key pair is generated for : {self.ownerName}.')
        logging.info("--------User Info Area--------")
        logging.info(
            'Please back up your key pair in order to keep an access to your transactions and wallet.')
        logging.info(f'Your key pair is exported as a json file.')
        logging.info("------------------------------")

    # Updating the Wallet's owner balance.

    def updateTransactions(self, blockchain: Blockchain):
        self.balance = blockchain.getBalance(self.publicKey)
        return f'balance in the Wallet: {self.balance}'

    def getBalance(self, blockchain) -> int:
        self.updateTransactions(blockchain)
        return self.balance


class WalletChecker():
    Wallets = []

    def __init__(self, Wallets: list):
        self.Wallets = Wallets

    def addWallet(self, newWallet: Wallet):
        for Wallet in self.Wallets:
            if Wallet.publicAddress == newWallet.publicAddress:
                logging.warning(
                    "WalletChecker: You can't use an existed Wallet name!")
                return

        self.Wallets.append(newWallet)
