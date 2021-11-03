from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import json
import pathlib
from Blockchain import Blockchain


# A general purpose wallet for blockchain.

class Wallet():
    ownerName = ''
    publicKey = ''  # aka source
    privateKey = ''
    coins = 0
    creationTime = None

    def __init__(self, ownerName: str):
        self.ownerName = ownerName

    def createNewWallet(self):
        self.creationTime = datetime.now().strftime("%H:%M:%S")
        self.generateKeyPair()
        self.exportKeyPair()
        self.done()

    def generateKeyPair(self):
        randomGenerator = Random.new().read
        keyPair = RSA.generate(1024, randomGenerator)
        privateKey = keyPair.exportKey('PEM')
        self.privateKey = base64.b64encode(privateKey).decode("ascii")

        publicKey = keyPair.publickey().exportKey('PEM')
        self.publicKey = base64.b64encode(publicKey).decode("ascii")

        # Here we shorten public key by removing the trivial parts.
        self.publicKey = self.publicKey[87:-44]

    def exportKeyPair(self):
        keypair = {
            "wallet_user_name": self.ownerName,
            "public_key": self.publicKey,
            "private_key": self.privateKey
        }
        pathlib.Path('./key_pair_exports').mkdir(exist_ok=True)
        with open('./key_pair_exports/' + self.ownerName + '_key_pair.json', 'w', encoding='utf-8') as f:
            json.dump(keypair, f, ensure_ascii=False, indent=4)

    def done(self):
        print(
            f'A new public and private key pair is generated for : {self.ownerName}.')
        print(
            'Please back up your key pair in order to keep an access to your transactions and wallet.')
        print(f'Your key pair is exported as a json file.\n')

    # Updating the Wallet's owner balance.

    def updateTransactions(self, blockchain: Blockchain):
        self.coins = blockchain.getBalance(self.publicKey)
        return f'Coins in the Wallet: {self.coins}'


class WalletChecker():
    Wallets = []

    def __init__(self, Wallets: list):
        self.Wallets = Wallets

    def addWallet(self, newWallet: Wallet):
        for Wallet in self.Wallets:
            if Wallet.publicAddress == newWallet.publicAddress:
                print("You can't use an existed Wallet name!")
                return

        self.Wallets.append(newWallet)
